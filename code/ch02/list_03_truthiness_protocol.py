"""リスト2-3: 真偽判定は`__len__`・`__bool__`のプロトコルに従う。

`if obj:` はまず`__bool__`を、それが無ければ`__len__`を呼び出し、
どちらも定義されていないオブジェクトは常にtruthyとして扱われる。
JavaやC#の「参照はnull以外なら真」という単純な規則とは異なり、
Pythonでは自作クラスも「空かどうか」で真偽を制御できる。
"""


class SizedContainer:
    """`__len__`だけを実装し、要素数0のときfalsyになるクラス。"""

    def __init__(self, size: int) -> None:
        self._size = size

    def __len__(self) -> int:
        return self._size


class AlwaysTruthy:
    """`__len__`も`__bool__`も持たないため、常にtruthyになるクラス。"""
