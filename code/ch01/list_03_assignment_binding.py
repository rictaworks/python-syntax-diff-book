"""リスト1-3: 代入は「名前の束縛」である。

`b = a` は値のコピーではなく、同じオブジェクトに
2つ目の名前を束縛する操作である。そのため、bを介した
可変オブジェクトの変更はaからも見える。詳細は第2章。
"""


def append_and_share(source: list, value: object) -> list:
    """sourceに要素を追加し、同じオブジェクトを返す。"""
    source.append(value)
    return source
