"""リスト2-2: 代入は式ではなく文である。

C系言語やJavaScriptでは `if (x = 5)` のように代入を式として
条件式の中に埋め込めるが、Pythonの `=` は文専用であり式の位置には
書けない。値を束縛しつつ式としても使いたい場合は、Python 3.8以降の
海象演算子 `:=`（代入式）を使う。
"""


def build_assignment_in_condition_source() -> str:
    """if文の条件式に単純代入 `=` を書いたソースコード文字列を返す。"""
    return (
        "x = 1\n"
        "if x = 5:\n"
        "    pass\n"
    )


def compile_snippet(source: str):
    """文字列をコンパイルする（実行はしない）。"""
    return compile(source, "<snippet>", "exec")


def evaluate_with_walrus(x: int) -> int | None:
    """海象演算子で束縛した値を条件式の中でそのまま使う。"""
    if (doubled := x * 2) > 10:
        return doubled
    return None
