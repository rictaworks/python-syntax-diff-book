"""リスト1-5: list・tuple・dict・setの使い分けと内包表記。

Pythonにはmap・filter相当の変換を1行で書くための内包表記
（comprehension）が第一級の構文として存在する。list・tuple・
dict・setの使い分けと内包表記の詳細は第3章で扱う。
"""


def squares_under(limit: int) -> list[int]:
    """0以上limit未満の整数の2乗を内包表記で返す。"""
    return [n * n for n in range(limit)]
