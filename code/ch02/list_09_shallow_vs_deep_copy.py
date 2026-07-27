"""リスト2-9: 浅いコピーと深いコピーの違い。

`copy.copy()`は最も外側の入れ物だけを複製し、内側の可変オブジェクト
は元のオブジェクトと共有し続ける（浅いコピー）。`copy.deepcopy()`は
入れ子になったオブジェクトまで再帰的に複製する（深いコピー）。
「コピーしたつもり」でも浅いコピーでは変更が伝播することがある。
"""

import copy


def shallow_copy_nested_list(source: list) -> list:
    """最も外側のlistだけを複製する（内側のlistは共有される）。"""
    return copy.copy(source)


def deep_copy_nested_list(source: list) -> list:
    """入れ子のlistまで再帰的に複製する。"""
    return copy.deepcopy(source)
