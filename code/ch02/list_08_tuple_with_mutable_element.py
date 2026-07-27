"""リスト2-8: tupleは「浅く」不変である。

tuple自体は要素の差し替えを許さないが、それは「tupleが指している
オブジェクトの集合を変えられない」という意味にとどまる。要素として
listのような可変オブジェクトを持てば、そのlistの中身は変更できる。
「不変」は再帰的な保証ではない。
"""


def build_point_with_mutable_tail() -> tuple:
    """1つ目がint、2つ目がlistの2要素tupleを返す。"""
    return (1, [2, 3])


def reassign_first_element(point: tuple, value: object) -> tuple:
    """tupleの要素を差し替えようとする（失敗しTypeErrorになる）。"""
    point[0] = value
    return point


def append_to_tail(point: tuple, value: object) -> tuple:
    """tuple自体は変えず、2つ目の要素であるlistへ追加する。"""
    point[1].append(value)
    return point
