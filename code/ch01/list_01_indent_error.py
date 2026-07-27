"""リスト1-1: ブロックはインデントで表す。

他言語の { } や end と異なり、Pythonではインデントの
深さ自体が構文の一部になる。深さが揃わない行は、実行前の
コンパイル時点で IndentationError になる。
"""


def build_mis_indented_source() -> str:
    """字下げが1行だけずれたソースコード文字列を返す。"""
    return (
        "def greet():\n"
        "    print('a')\n"
        "  print('b')\n"
    )


def compile_snippet(source: str):
    """文字列をコンパイルする（実行はしない）。"""
    return compile(source, "<snippet>", "exec")
