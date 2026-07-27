"""リスト1-9: importは実行文であり、モジュールは一度だけ実行される。

importは宣言ではなく実行文であり、最初にimportされた時点で
トップレベルのコードが1度だけ実行される。以降のimportは
sys.modulesにキャッシュされたモジュールオブジェクトを再利用
するだけである。importの実行モデルの詳細は第10章で扱う。
"""

import_log: list[str] = []
import_log.append("executed")
