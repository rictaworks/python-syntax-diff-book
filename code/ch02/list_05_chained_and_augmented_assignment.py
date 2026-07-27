"""リスト2-5: 連鎖代入と累算代入で見える束縛の実態。

`a = b = c = []` は3つの名前が同じ1つのオブジェクトに束縛される
連鎖代入である。一方、累算代入（`+=`）の挙動はオブジェクトが不変か
可変かで分かれる。intへの`+=`は新しいintオブジェクトを作って
再束縛するが、listへの`+=`は同じオブジェクトを書き換える。
"""


def bind_same_list_to_three_names() -> tuple[list, list, list]:
    """連鎖代入で3つの名前を同じ空listに束縛して返す。"""
    a = b = c = []
    return a, b, c


def increment_and_track_identity(value: int) -> tuple[int, bool]:
    """intへの`+=`前後で`id()`が変わることを確認する。"""
    before_id = id(value)
    value += 1
    after_id = id(value)
    return value, before_id == after_id


def append_and_track_identity(
    items: list, value: object
) -> tuple[list, bool]:
    """listへの`+=`前後で`id()`が変わらないことを確認する。"""
    before_id = id(items)
    items += [value]
    after_id = id(items)
    return items, before_id == after_id
