#!/usr/bin/env bash
#
# build/epub.sh
#
# manuscript/ 配下のMarkdown原稿を目次順に結合し、リフロー型EPUB
# （Kindle対応）を生成する。CIの「Validate EPUB build」ステップと
# ローカル実行が同じ手順・同じ結果になるよう、ローカル/CIの両方から
# 本スクリプト1本だけを呼び出す設計にしている。
#
# 手順:
#   1. 依存コマンド（pandoc / java / python3）の存在確認
#   2. コード桁数lint（build/lint_code_width.py）の実行
#   3. Pandocによる EPUB3 生成
#   4. EPUBCheckによる検証
#
# 設定値（タイトル・出力先・しきい値など）はすべて
# build/config/epub-build.env に分離している。本スクリプトに
# 文字列・数値のハードコードは含めない。
#
# フォールバックは行わない。依存コマンドが無い／ビルドや検証に
# 失敗した場合は、原因を推測で補わずその場でエラー終了する。

set -euo pipefail

# --- ログ関数 -----------------------------------------------------

log_info() {
    local message="$1"
    printf '[INFO] %s\n' "${message}"
}

log_error() {
    local message="$1"
    printf '[ERROR] %s\n' "${message}" >&2
}

log_debug() {
    local message="$1"
    if [[ "${EPUB_BUILD_VERBOSE:-0}" == "1" ]]; then
        printf '[DEBUG] %s\n' "${message}" >&2
    fi
}

# --- 依存コマンドの確認 ---------------------------------------------

require_command() {
    local command_name="$1"
    local install_hint="$2"
    if ! command -v "${command_name}" >/dev/null 2>&1; then
        log_error "必須コマンドが見つかりません: ${command_name}"
        log_error "対処: ${install_hint}"
        exit 1
    fi
    log_debug "コマンド確認OK: ${command_name}"
}

# --- 設定読み込み ---------------------------------------------------

load_build_config() {
    local repo_root="$1"
    local config_path="${repo_root}/build/config/epub-build.env"

    if [[ ! -f "${config_path}" ]]; then
        log_error "ビルド設定ファイルが見つかりません: ${config_path}"
        exit 1
    fi

    # shellcheck source=build/config/epub-build.env
    set -a
    # shellcheck disable=SC1090
    source "${config_path}"
    set +a
    log_debug "ビルド設定を読み込みました: ${config_path}"
}

# --- EPUBCheckの実行コマンド解決 -------------------------------------
#
# Debian/Ubuntu の epubcheck パッケージは /usr/bin/epubcheck が
# 素のjarファイルへのシンボリックリンクになっていることがあり、
# その場合は直接実行できない。EPUBCHECK_JAR_PATH に実体があれば
# `java -jar` 経由で呼び出す。

resolve_epubcheck_invocation() {
    local jar_path="$1"

    if [[ -f "${jar_path}" ]]; then
        printf 'java -jar %s' "${jar_path}"
        return 0
    fi

    if command -v epubcheck >/dev/null 2>&1; then
        printf 'epubcheck'
        return 0
    fi

    log_error "epubcheckを実行できません（jar未検出: ${jar_path} / epubcheckコマンドも未検出）"
    log_error "対処: sudo apt-get install -y epubcheck default-jre-headless"
    exit 1
}

# --- 原稿ファイル収集 -------------------------------------------------

collect_manuscript_files() {
    local repo_root="$1"
    local manuscript_dir="$2"
    local target_dir="${repo_root}/${manuscript_dir}"

    if [[ ! -d "${target_dir}" ]]; then
        log_error "原稿ディレクトリが見つかりません: ${target_dir}"
        exit 1
    fi

    find "${target_dir}" -maxdepth 1 -type f -name '*.md' | LC_ALL=C sort
}

# --- 図版ラスタライズ ---------------------------------------------------
#
# KindleのフォーマットはSVG/SVGZの図版埋め込みに対応していない
# （EPUBCheckはEPUB3構造として合格するが、Kindle Previewerでの実機
# 変換がE21018で失敗する）。そのためfigures/配下を丸ごとキャッシュへ
# ミラーリングし、SVGだけをrsvg-convertでPNGへ変換する。それ以外の
# ファイルはそのままコピーする。manuscript/・figures/ 配下の実ファイル
# は変更しない。

rasterize_figures_directory() {
    local repo_root="$1"
    local figures_dir="$2"
    local raster_cache_dir="$3"

    local source_dir="${repo_root}/${figures_dir}"
    local target_dir="${raster_cache_dir}/${figures_dir}"

    if [[ ! -d "${source_dir}" ]]; then
        log_error "図版ディレクトリが見つかりません: ${source_dir}"
        exit 1
    fi

    rm -rf "${target_dir}"
    mkdir -p "${target_dir}"

    local svg_file
    while IFS= read -r svg_file; do
        local rel_path="${svg_file#${source_dir}/}"
        local png_path="${target_dir}/${rel_path%.svg}.png"
        mkdir -p "$(dirname "${png_path}")"
        log_debug "SVGをPNGへ変換します: ${rel_path}"
        rsvg-convert "${svg_file}" -o "${png_path}"
    done < <(find "${source_dir}" -type f -name '*.svg')

    local other_file
    while IFS= read -r -d '' other_file; do
        local rel_path="${other_file#${source_dir}/}"
        local dest_path="${target_dir}/${rel_path}"
        mkdir -p "$(dirname "${dest_path}")"
        cp "${other_file}" "${dest_path}"
    done < <(find "${source_dir}" -type f -not -name '*.svg' -print0)

    log_info "図版ラスタライズ完了: ${source_dir} -> ${target_dir}"
}

# --- 原稿のSVG参照書き換え ------------------------------------------------
#
# manuscript/配下の原稿をキャッシュへコピーし、Markdown画像記法内の
# `.svg)` 参照のみを `.png)` に書き換える。コピー先はキャッシュ内の
# manuscript/ ディレクトリとし、キャッシュ内のfigures/ ディレクトリと
# 相対位置（`../figures/...`）が原本と一致するようにする。

rewrite_manuscript_svg_references() {
    local raster_cache_dir="$1"
    local manuscript_dir="$2"
    shift 2
    local source_manuscript_files=("$@")

    local target_dir="${raster_cache_dir}/${manuscript_dir}"
    rm -rf "${target_dir}"
    mkdir -p "${target_dir}"

    local source_file
    for source_file in "${source_manuscript_files[@]}"; do
        local file_name
        file_name="$(basename "${source_file}")"
        local target_file="${target_dir}/${file_name}"
        sed 's/\.svg)/.png)/g' "${source_file}" > "${target_file}"
        printf '%s\n' "${target_file}"
    done
}

# --- コード桁数lint ---------------------------------------------------

run_code_width_lint() {
    local repo_root="$1"
    local lint_script="$2"
    local lint_config="$3"

    log_info "コード桁数lintを実行します: ${lint_script}"
    if ! python3 "${repo_root}/${lint_script}" \
        --repo-root "${repo_root}" \
        --config "${repo_root}/${lint_config}"; then
        log_error "コード桁数lintに失敗しました（原稿のコードリストが桁数上限を超過しています）"
        exit 1
    fi
    log_info "コード桁数lint: OK"
}

# --- Pandocメタデータの生成 --------------------------------------------

render_pandoc_metadata() {
    local metadata_path="$1"
    local title="$2"
    local subtitle="$3"
    local author="$4"
    local language="$5"

    cat > "${metadata_path}" <<EOF_METADATA
---
title: "${title}"
subtitle: "${subtitle}"
author: "${author}"
language: ${language}
---
EOF_METADATA
}

# --- EPUBビルド本体 ---------------------------------------------------

build_epub_with_pandoc() {
    local repo_root="$1"
    local metadata_path="$2"
    local output_path="$3"
    local split_level="$4"
    local target_format="$5"
    local style_css_path="$6"
    shift 6
    local manuscript_files=("$@")

    local pandoc_args=(
        "${metadata_path}"
        "${manuscript_files[@]}"
        -o "${output_path}"
        --toc
        --split-level="${split_level}"
        -t "${target_format}"
        --resource-path="${repo_root}/manuscript:${repo_root}"
    )

    if [[ -f "${style_css_path}" ]]; then
        log_info "スタイルシートを適用します: ${style_css_path}"
        pandoc_args+=(--css "${style_css_path}")
    else
        log_info "スタイルシートが見つからないため既定スタイルで生成します: ${style_css_path}"
    fi

    log_info "Pandocで${#manuscript_files[@]}件の原稿を結合します"
    pandoc "${pandoc_args[@]}"
}

# --- EPUBCheckによる検証 -------------------------------------------------

run_epubcheck() {
    local epubcheck_invocation="$1"
    local output_path="$2"

    log_info "EPUBCheckで検証します: ${output_path}"
    # shellcheck disable=SC2086
    if ! ${epubcheck_invocation} "${output_path}"; then
        log_error "EPUBCheckでエラーが検出されました: ${output_path}"
        exit 1
    fi
    log_info "EPUBCheck: OK（エラー0件）"
}

# --- メイン処理 ---------------------------------------------------------

main() {
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local repo_root
    repo_root="$(cd "${script_dir}/.." && pwd)"

    require_command "pandoc" "sudo apt-get install -y pandoc"
    require_command "java" "sudo apt-get install -y default-jre-headless"
    require_command "python3" "python3をインストールしてください（devcontainer利用時は自動導入済み）"
    require_command "rsvg-convert" "sudo apt-get install -y librsvg2-bin"

    load_build_config "${repo_root}"

    local epubcheck_invocation
    epubcheck_invocation="$(resolve_epubcheck_invocation "${EPUBCHECK_JAR_PATH}")"

    local manuscript_files_raw
    manuscript_files_raw="$(collect_manuscript_files "${repo_root}" "${MANUSCRIPT_DIR}")"
    if [[ -z "${manuscript_files_raw}" ]]; then
        log_error "原稿ファイルが1件も見つかりませんでした: ${repo_root}/${MANUSCRIPT_DIR}"
        exit 1
    fi
    local manuscript_files=()
    while IFS= read -r line; do
        manuscript_files+=("${line}")
    done <<< "${manuscript_files_raw}"
    log_info "結合対象（目次順）:"
    local manuscript_file
    for manuscript_file in "${manuscript_files[@]}"; do
        log_info "  - ${manuscript_file#${repo_root}/}"
    done

    run_code_width_lint "${repo_root}" "${LINT_SCRIPT_RELATIVE_PATH}" "${LINT_CONFIG_RELATIVE_PATH}"

    local raster_cache_dir="${repo_root}/${RASTER_CACHE_DIR}"
    rasterize_figures_directory "${repo_root}" "${FIGURES_DIR}" "${raster_cache_dir}"

    local rasterized_manuscript_files_raw
    rasterized_manuscript_files_raw="$(rewrite_manuscript_svg_references \
        "${raster_cache_dir}" "${MANUSCRIPT_DIR}" "${manuscript_files[@]}")"
    local rasterized_manuscript_files=()
    while IFS= read -r line; do
        rasterized_manuscript_files+=("${line}")
    done <<< "${rasterized_manuscript_files_raw}"

    local output_dir="${repo_root}/${OUTPUT_DIR}"
    mkdir -p "${output_dir}"
    local metadata_path="${output_dir}/.pandoc-metadata.yaml"
    local output_path="${output_dir}/${OUTPUT_FILENAME}"

    render_pandoc_metadata "${metadata_path}" "${EPUB_TITLE}" "${EPUB_SUBTITLE}" \
        "${EPUB_AUTHOR}" "${EPUB_LANGUAGE}"

    build_epub_with_pandoc "${raster_cache_dir}" "${metadata_path}" "${output_path}" \
        "${PANDOC_SPLIT_LEVEL}" "${PANDOC_TARGET_FORMAT}" \
        "${repo_root}/${STYLE_CSS_RELATIVE_PATH}" "${rasterized_manuscript_files[@]}"

    run_epubcheck "${epubcheck_invocation}" "${output_path}"

    log_info "EPUBビルド成功: ${output_path}"
}

main "$@"
