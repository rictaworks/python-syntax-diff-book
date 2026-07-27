"""manuscript配下のコードリストの桁数（列幅）を検査するスクリプト。

Kindleのリフロー型EPUBでは横スクロールができないため、コードリストの
1行が長すぎると右端が画面外に隠れて読めなくなる。本スクリプトは
Markdownのフェンスコードブロック（```python や ```pycon など）の内側
だけを対象に、各行の文字数が上限を超えていないかを検査する。

しきい値・対象言語・対象ディレクトリはすべて build/config/lint-width.json
に分離しており、本ファイル内に数値・文字列のハードコードはない。

終了コード:
    0: 違反なし
    1: 桁数超過あり、または設定・入力に不備があり検査を継続できない

使い方:
    python build/lint_code_width.py
    python build/lint_code_width.py --verbose
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

_LOGGER_NAME = "lint_code_width"


def get_logger() -> logging.Logger:
    """モジュール共通のロガーを取得する。

    モジュールレベルの可変なグローバル状態を持たないよう、ロガー
    インスタンスは都度 logging.getLogger() から取得する（同名なら
    同一インスタンスが返るためコストはない）。
    """
    return logging.getLogger(_LOGGER_NAME)


@dataclass(frozen=True)
class LintConfig:
    """lint-width.json の内容を表す設定値。"""

    max_line_width: int
    target_fence_languages: tuple[str, ...]
    target_directory: str


@dataclass(frozen=True)
class WidthViolation:
    """1行分の桁数超過を表す。"""

    file_path: Path
    line_number: int
    fence_language: str
    width: int
    max_line_width: int
    content: str

    def format_message(self) -> str:
        """人間が読める1行のエラーメッセージを作る。"""
        return (
            f"{self.file_path}:{self.line_number}: "
            f"{self.width}桁（上限{self.max_line_width}桁を超過） "
            f"[{self.fence_language}] {self.content}"
        )


def load_config(config_path: Path) -> LintConfig:
    """設定ファイル(JSON)を読み込む。

    フォールバックは行わない。ファイルが存在しない、またはキーが
    欠けている場合は、原因が分かる例外をそのまま送出する。
    """
    if not config_path.is_file():
        raise FileNotFoundError(f"lint設定ファイルが見つかりません: {config_path}")

    raw_text = config_path.read_text(encoding="utf-8")
    raw_data = json.loads(raw_text)

    try:
        return LintConfig(
            max_line_width=int(raw_data["max_line_width"]),
            target_fence_languages=tuple(raw_data["target_fence_languages"]),
            target_directory=str(raw_data["target_directory"]),
        )
    except KeyError as missing_key:
        raise KeyError(
            f"lint設定ファイルに必須キーがありません: {missing_key} ({config_path})"
        ) from missing_key


def iter_fenced_code_lines(markdown_text: str) -> Iterator[tuple[int, str, str]]:
    """Markdown本文からフェンスコードブロック内の行だけを取り出す。

    Yields:
        (1始まりの行番号, フェンス言語（```python の "python" 部分）, 行内容)
    """
    in_fence = False
    fence_language = ""
    for line_number, raw_line in enumerate(markdown_text.splitlines(), start=1):
        stripped_line = raw_line.rstrip("\n")
        if stripped_line.startswith("```"):
            if in_fence:
                in_fence = False
                fence_language = ""
            else:
                in_fence = True
                fence_language = stripped_line[3:].strip()
            continue
        if in_fence:
            yield line_number, fence_language, stripped_line


def find_width_violations(file_path: Path, config: LintConfig) -> list[WidthViolation]:
    """1ファイル分の桁数超過を検出する。"""
    markdown_text = file_path.read_text(encoding="utf-8")
    violations: list[WidthViolation] = []

    for line_number, fence_language, content in iter_fenced_code_lines(markdown_text):
        if fence_language not in config.target_fence_languages:
            continue
        width = len(content)
        if width > config.max_line_width:
            violations.append(
                WidthViolation(
                    file_path=file_path,
                    line_number=line_number,
                    fence_language=fence_language,
                    width=width,
                    max_line_width=config.max_line_width,
                    content=content,
                )
            )

    return violations


def collect_target_files(repo_root: Path, config: LintConfig) -> list[Path]:
    """対象ディレクトリ配下のMarkdownファイル一覧を、名前順で取得する。"""
    target_dir = repo_root / config.target_directory
    if not target_dir.is_dir():
        raise NotADirectoryError(f"lint対象ディレクトリが存在しません: {target_dir}")
    return sorted(target_dir.glob("*.md"))


def run_lint(repo_root: Path, config_path: Path) -> list[WidthViolation]:
    """lint本体。全対象ファイルを検査し、違反一覧を返す。"""
    logger = get_logger()
    config = load_config(config_path)
    logger.debug(
        "lint設定を読み込みました: max_line_width=%d, target_fence_languages=%s, "
        "target_directory=%s",
        config.max_line_width,
        config.target_fence_languages,
        config.target_directory,
    )

    target_files = collect_target_files(repo_root, config)
    logger.info("桁数lint 検査対象ファイル数: %d", len(target_files))

    all_violations: list[WidthViolation] = []
    for file_path in target_files:
        violations = find_width_violations(file_path, config)
        logger.debug("%s: %d件の違反", file_path, len(violations))
        all_violations.extend(violations)

    return all_violations


def parse_args(argv: list[str]) -> argparse.Namespace:
    """コマンドライン引数を解釈する。"""
    default_repo_root = Path(__file__).resolve().parent.parent
    default_config_path = default_repo_root / "build" / "config" / "lint-width.json"

    parser = argparse.ArgumentParser(
        description="manuscript配下のコードリストの桁数を検査する。"
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=default_repo_root,
        help="リポジトリルート（既定: このスクリプトの2階層上）",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=default_config_path,
        help="lint設定JSONのパス（既定: build/config/lint-width.json）",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="デバッグトレースを出力する",
    )
    return parser.parse_args(argv)


def configure_logging(verbose: bool) -> None:
    """デバッグトレース用のログ出力を設定する。"""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s %(name)s: %(message)s",
    )


def main(argv: list[str] | None = None) -> int:
    """エントリポイント。違反があれば1、なければ0を返す。"""
    args = parse_args(list(argv) if argv is not None else sys.argv[1:])
    configure_logging(args.verbose)
    logger = get_logger()

    violations = run_lint(args.repo_root, args.config)

    if violations:
        logger.error("桁数超過が%d件見つかりました。", len(violations))
        for violation in violations:
            logger.error(violation.format_message())
        return 1

    logger.info("桁数lint: 違反なし。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
