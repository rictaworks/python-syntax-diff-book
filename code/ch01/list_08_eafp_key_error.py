"""リスト1-8: 例外を使った制御フロー（EAFP）。

「まず確認してから実行する」（LBYL）ではなく、「まず試して、
失敗したら例外で対処する」（EAFP）がPythonの定石である。
EAFPの詳細は第8章で扱う。
"""


def price_or_default(prices: dict[str, int], item: str) -> int:
    """キーの有無を事前確認せず、まず取得を試みる（EAFP）。"""
    try:
        return prices[item]
    except KeyError:
        return 0
