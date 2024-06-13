"""
赤外線のsendするモジュール
"""

import subprocess  # subprocessモジュールをインポートして、サブプロセスを管理する

# 赤外線コマンドを送信するためのコマンドを定義
command = ["cgir", "send", "light:on", "-g", "21"]
# subprocess.call()を使用して、コマンドを実行
subprocess.call(command)

# ir_sender.py
# このスクリプトの名前（ファイル名）は「ir_sender.py」

import subprocess  # subprocessモジュールをインポートして、サブプロセスを管理する

def send_ir_command():
    """
    cgirツールを使用して赤外線コマンドを送信します。
    """
    # 赤外線コマンドを送信するためのコマンドを定義
    command = ["cgir", "send", "light:on", "-g", "21"]
    # subprocess.call()を使用して、コマンドを実行
    subprocess.call(command)

if __name__ == "__main__":
    # このブロックはスクリプトが直接実行された場合にのみ実行されます
    send_ir_command()
    # send_ir_command()関数を呼び出して、赤外線コマンドを送信する
