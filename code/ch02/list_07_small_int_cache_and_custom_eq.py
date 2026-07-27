"""リスト2-7: `is`と`==`は別の質問に答える。

`==`は「値が等しいか」、`is`は「同一のオブジェクトか」を尋ねる。
CPythonは-5〜256の小さなintを実装の最適化としてキャッシュして
使い回すため、この範囲では別々に生成しても`is`がTrueになりうる
（言語仕様ではなくCPython実装の詳細であり、保証された挙動ではない）。
範囲外では同じ値でも別オブジェクトになりうる。加えて、`__eq__`を
独自定義すれば`==`の結果は同一性と無関係に決められる。
"""


def create_two_ints_via_separate_compilations(
    value: int,
) -> tuple[int, int]:
    """同じ整数値を、独立した2つのコンパイル単位でそれぞれ生成する。

    同一のソース文字列内に同じリテラルを2回書くと、定数畳み込みに
    よって意図せず同じオブジェクトが再利用されてしまう。それを避ける
    ため、あえて2つの独立した名前空間でそれぞれexecする。
    """
    namespace_a: dict = {}
    namespace_b: dict = {}
    source = f"result = {value}"
    exec(compile(source, "<ns_a>", "exec"), namespace_a)
    exec(compile(source, "<ns_b>", "exec"), namespace_b)
    return namespace_a["result"], namespace_b["result"]


class AlwaysEqual:
    """`__eq__`を常にTrueへ固定し、`==`と`is`を意図的に乖離させるクラス。"""

    def __eq__(self, other: object) -> bool:
        return True
