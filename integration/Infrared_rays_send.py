"""
赤外線のsendするモジュール
"""

import subprocess

command = ["cgir", "send", "light:on", "-g", "21"]
subprocess.call(command)

# ir_sender.py

import subprocess

def send_ir_command():
    """
    cgirツールを使用して赤外線コマンドを送信します。
    """
    command = ["cgir", "send", "light:on", "-g", "21"]
    subprocess.call(command)

if __name__ == "__main__":
    # このブロックはスクリプトが直接実行された場合にのみ実行されます
    send_ir_command()