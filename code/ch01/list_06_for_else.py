"""リスト1-6: forは常にforeachであり、for-elseとmatch文がある。

C系言語のインデックス制御forはPythonに存在せず、forは常に
foreachである。加えて、breakされずにforを終えたときだけ
実行されるelse節がある。forとmatch文の詳細は第4章で扱う。
"""


def find_first_negative(values: list[int]) -> str:
    """breakされずにforを終えたときだけelse節が実行される。"""
    for value in values:
        if value < 0:
            message = f"found: {value}"
            break
    else:
        message = "no negative value"
    return message
