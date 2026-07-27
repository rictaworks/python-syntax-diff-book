"""リスト1-2: 真偽判定とNoneの扱い。

if文の条件は真偽値だけでなく、0・空文字列・空リスト・None
なども「falsy」として偽扱いになる。Noneはnull/nil/undefined
に近いが、シングルトンであり、Falseとも0とも等しくない。
"""


def classify_truthiness(values: list) -> list[bool]:
    """各要素をbool()で判定した結果のリストを返す。"""
    return [bool(value) for value in values]
