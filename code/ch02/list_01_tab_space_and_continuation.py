"""リスト2-1: インデントの深さと、タブ・スペース混在のTabError。

Pythonのブロックはインデントの「深さ」で決まるが、深さの比較には
タブとスペースの混在を許さない場合がある。1行目をタブ、2行目を
スペースだけの字下げにすると、字下げの深さが一意に決まらず
TabErrorになる。あわせて、丸括弧の中では改行してもバックスラッシュ
なしで1つの式として続けられる（暗黙の行継続）ことも確認する。
"""


def build_tab_space_mixed_source() -> str:
    """タブとスペースが混在した字下げのソースコード文字列を返す。"""
    return (
        "def f():\n"
        "\tprint('a')\n"
        "        print('b')\n"
    )


def compile_snippet(source: str):
    """文字列をコンパイルする（実行はしない）。"""
    return compile(source, "<snippet>", "exec")


def sum_across_continued_lines(
    first: int, second: int, third: int
) -> int:
    """丸括弧内での暗黙の行継続を使い、複数行にまたがる式を1つ返す。"""
    return (
        first
        + second
        + third
    )
