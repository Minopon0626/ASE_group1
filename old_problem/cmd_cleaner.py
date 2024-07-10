import os
import subprocess

def clear_cmd_screen():
    """cmd.exeの画面をクリアする関数"""
    try:
        # clsコマンドを実行して画面をクリア
        subprocess.run("cls", shell=True, check=True)
        print("画面がクリアされました。")
    except subprocess.CalledProcessError as e:
        print(f"画面のクリアに失敗しました: {e}")

if __name__ == "__main__":
    clear_cmd_screen()
