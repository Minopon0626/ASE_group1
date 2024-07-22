import subprocess
import os

def send_ir_command(signal_name = 'light:on'):
    """
    cgirツールを使用して指定された赤外線コマンドを送信します。
    
    :param signal_name: 送信する信号の名前（例: "light:on"）
    """
    # スクリプトのディレクトリを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # code.jsonのパスを生成
    json_path = os.path.join(script_dir, "code.json")

    # 赤外線コマンドを送信するためのコマンドを定義
    command = ["cgir", "send", signal_name, "-g", "21", "-f", json_path]
    
    # subprocess.run()を使用して、コマンドを実行
    result = subprocess.run(command, capture_output=True, text=True)

    # コマンドの標準出力と標準エラーを表示
    print("標準出力:", result.stdout)
    print("標準エラー:", result.stderr)

if __name__ == "__main__":
    send_ir_command('light:on')
