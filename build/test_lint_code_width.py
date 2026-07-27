"""build/lint_code_width.py の検証テスト。

GitHub Issue #8「EPUBビルド基盤を整備する」の受け入れ条件
「コード桁数lintが60〜70桁超過時に失敗するよう機能すること」を
実際に確認する。
"""

import json
from pathlib import Path

import pytest
from lint_code_width import (
    LintConfig,
    collect_target_files,
    find_width_violations,
    iter_fenced_code_lines,
    load_config,
    run_lint,
)


def test_load_config_reads_expected_keys(tmp_path: Path) -> None:
    config_path = tmp_path / "lint-width.json"
    config_path.write_text(
        json.dumps(
            {
                "max_line_width": 70,
                "target_fence_languages": ["python", "pycon"],
                "target_directory": "manuscript",
            }
        ),
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config == LintConfig(
        max_line_width=70,
        target_fence_languages=("python", "pycon"),
        target_directory="manuscript",
    )


def test_load_config_raises_when_file_missing(tmp_path: Path) -> None:
    missing_path = tmp_path / "does-not-exist.json"
    with pytest.raises(FileNotFoundError):
        load_config(missing_path)


def test_load_config_raises_when_key_missing(tmp_path: Path) -> None:
    config_path = tmp_path / "lint-width.json"
    config_path.write_text(json.dumps({"max_line_width": 70}), encoding="utf-8")

    with pytest.raises(KeyError):
        load_config(config_path)


def test_iter_fenced_code_lines_only_yields_inside_fences() -> None:
    markdown_text = "\n".join(
        [
            "# title",
            "prose line, not code",
            "```python",
            "def f():",
            "    return 1",
            "```",
            "prose after",
        ]
    )

    result = list(iter_fenced_code_lines(markdown_text))

    assert result == [
        (4, "python", "def f():"),
        (5, "python", "    return 1"),
    ]


def test_find_width_violations_detects_line_over_limit(tmp_path: Path) -> None:
    long_line = "x = " + "a" * 70  # 74桁、上限70桁を超える
    markdown_path = tmp_path / "01-sample.md"
    markdown_path.write_text(
        "\n".join(["```python", long_line, "```", ""]),
        encoding="utf-8",
    )
    config = LintConfig(
        max_line_width=70,
        target_fence_languages=("python",),
        target_directory="manuscript",
    )

    violations = find_width_violations(markdown_path, config)

    assert len(violations) == 1
    assert violations[0].line_number == 2
    assert violations[0].width == len(long_line)


def test_find_width_violations_passes_when_within_limit(tmp_path: Path) -> None:
    short_line = "x = 1"
    markdown_path = tmp_path / "01-sample.md"
    markdown_path.write_text(
        "\n".join(["```python", short_line, "```", ""]),
        encoding="utf-8",
    )
    config = LintConfig(
        max_line_width=70,
        target_fence_languages=("python",),
        target_directory="manuscript",
    )

    violations = find_width_violations(markdown_path, config)

    assert violations == []


def test_find_width_violations_ignores_non_target_fence_language(tmp_path: Path) -> None:
    long_line = "a" * 100
    markdown_path = tmp_path / "01-sample.md"
    markdown_path.write_text(
        "\n".join(["```text", long_line, "```", ""]),
        encoding="utf-8",
    )
    config = LintConfig(
        max_line_width=70,
        target_fence_languages=("python", "pycon"),
        target_directory="manuscript",
    )

    violations = find_width_violations(markdown_path, config)

    assert violations == []


def test_collect_target_files_raises_when_directory_missing(tmp_path: Path) -> None:
    config = LintConfig(
        max_line_width=70,
        target_fence_languages=("python",),
        target_directory="no-such-dir",
    )

    with pytest.raises(NotADirectoryError):
        collect_target_files(tmp_path, config)


def test_run_lint_fails_on_real_manuscript_directory_with_lowered_limit(
    tmp_path: Path,
) -> None:
    """しきい値を意図的に下げ、既存原稿でも桁数lintが失敗として機能することを確認する。"""
    repo_root = Path(__file__).resolve().parent.parent
    config_path = tmp_path / "lint-width.json"
    config_path.write_text(
        json.dumps(
            {
                "max_line_width": 10,
                "target_fence_languages": ["python", "pycon"],
                "target_directory": "manuscript",
            }
        ),
        encoding="utf-8",
    )

    violations = run_lint(repo_root, config_path)

    assert len(violations) > 0


def test_run_lint_passes_on_real_manuscript_directory_with_shipped_config() -> None:
    """リポジトリ同梱のbuild/config/lint-width.jsonで、現行原稿が違反なしであることを確認する。"""
    repo_root = Path(__file__).resolve().parent.parent
    config_path = repo_root / "build" / "config" / "lint-width.json"

    violations = run_lint(repo_root, config_path)

    assert violations == []
