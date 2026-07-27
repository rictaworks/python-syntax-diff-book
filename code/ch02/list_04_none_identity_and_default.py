"""リスト2-4: `None`は唯一のシングルトンである。

`None`はプログラム全体でただ1つしか存在しないオブジェクトであり、
何度`id()`を取っても同じ値になる。この性質があるからこそ、
「値を渡されなかった」を表すデフォルト引数には`None`を使い、
`is None`で比較するのが慣用になる。
"""


def get_none_identity_pair() -> tuple[int, int]:
    """`None`の`id()`を2回取得し、そのペアを返す。"""
    return id(None), id(None)


def greet(name: str | None = None) -> str:
    """`name`が省略（`None`）なら既定の挨拶にする。"""
    if name is None:
        name = "world"
    return f"hello, {name}"
