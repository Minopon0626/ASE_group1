# pip install pigpio


import pigpio  # pigpioライブラリをインポート
import time  # timeライブラリをインポート

# 初期設定
pi = pigpio.pi()  # pigpioのインスタンスを作成
if not pi.connected:  # pigpioが接続されていない場合
    exit()  # スクリプトを終了

# 赤外線受信の設定
RX_PIN = 18  # 赤外線受信モジュールが接続されているGPIOピン番号
TX_PIN = 17  # 赤外線送信モジュールが接続されているGPIOピン番号
RECEIVE_TIME = 10  # 受信時間（秒）

# 赤外線信号を受信するクラス
class IRReceiver:
    def __init__(self, pi, rx_pin):
        self.pi = pi  # pigpioインスタンスを保存
        self.rx_pin = rx_pin  # 受信ピンを保存
        self.data = []  # 受信データを保存するリストを初期化
        self.callback = pi.callback(rx_pin, pigpio.FALLING_EDGE, self._cb)  # FALLING_EDGEイベントにコールバック関数を登録

    def _cb(self, gpio, level, tick):
        self.data.append(tick)  # タイムスタンプをデータリストに追加

    def get_data(self):
        return self.data  # 受信データを返す

    def clear_data(self):
        self.data = []  # 受信データをクリア

# 赤外線信号を送信する関数
def send_ir_signal(pi, tx_pin, data):
    if len(data) < 2:  # データが2つ未満の場合は処理を終了
        return

    carrier_freq = 38000  # キャリア周波数（Hz）
    gap = data[1] - data[0]  # 最初のギャップを計算
    pulses = []  # パルスリストを初期化

    for i in range(2, len(data)):  # データリストの2番目以降の要素について
        pulses.append(data[i] - data[i-1])  # パルスの長さを計算して追加

    for pulse in pulses:  # パルスリストの各パルスについて
        pi.wave_add_generic([  # 波形データを追加
            pigpio.pulse(1 << tx_pin, 0, int(pulse / 2)),  # パルスのON部分
            pigpio.pulse(0, 1 << tx_pin, int(pulse / 2))  # パルスのOFF部分
        ])

    pi.wave_create()  # 波形を作成
    pi.wave_send_repeat(pi.wave_tx_at())  # 波形を繰り返し送信

# ログをファイルに保存する関数
def log_data_to_file(filename, data):
    with open(filename, 'w') as f:  # ファイルを開く（書き込みモード）
        for timestamp in data:  # データリストの各タイムスタンプについて
            f.write(f"{timestamp}\n")  # タイムスタンプをファイルに書き込む

# 赤外線信号の受信と送信
receiver = IRReceiver(pi, RX_PIN)  # IRReceiverインスタンスを作成
print("赤外線信号を受信中...")  # 受信開始メッセージを表示
time.sleep(RECEIVE_TIME)  # 指定時間（10秒）待機して信号を受信
data = receiver.get_data()  # 受信データを取得
receiver.clear_data()  # 受信データをクリア
print("受信完了")  # 受信完了メッセージを表示

# ログファイルに記録
log_file = "log.txt"  # ログファイルの名前を設定
log_data_to_file(log_file, data)  # 受信データをログファイルに記録
print(f"受信したデータを {log_file} に記録しました。")  # ログファイルへの記録完了メッセージを表示

if data:  # 受信データがある場合
    print("赤外線信号を送信中...")  # 送信開始メッセージを表示
    send_ir_signal(pi, TX_PIN, data)  # 受信データを送信
    print("送信完了")  # 送信完了メッセージを表示

# 終了処理
pi.stop()  # pigpioを停止
