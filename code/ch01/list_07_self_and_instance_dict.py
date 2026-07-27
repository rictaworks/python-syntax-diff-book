"""リスト1-7: selfの明示、属性は辞書、ダックタイピング。

Javaのthis・Rubyのselfは暗黙に参照できるが、Pythonの
インスタンスメソッドは第一引数selfを自分で明記する。
インスタンス属性の実体は多くの場合__dict__という辞書である。
selfの明示・属性辞書・ダックタイピングの詳細は第7章で扱う。
"""


class Counter:
    """selfを明記した最小限のクラス。"""

    def __init__(self, start: int) -> None:
        self.value = start

    def bump(self) -> None:
        self.value += 1
