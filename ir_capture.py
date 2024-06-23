# 必要なライブラリ
# sudo apt-get update
# sudo apt-get install pigpio python3-pigpio

import pigpio
import time

# 受信データを保存するリスト
ir_data = []

# コールバック関数
def ir_callback(gpio, level, tick):
    global ir_data
    ir_data.append((level, tick))

# Pigpioの初期化
pi = pigpio.pi()
if not pi.connected:
    exit()

# 赤外線受信モジュールのGPIOピン番号
ir_gpio_pin = 18

# コールバックを設定
pi.set_mode(ir_gpio_pin, pigpio.INPUT)
pi.callback(ir_gpio_pin, pigpio.EITHER_EDGE, ir_callback)

# 受信待機時間（秒）
wait_time = 10

print(f"Listening for IR signal for {wait_time} seconds...")
time.sleep(wait_time)

# Pigpioの終了
pi.stop()

# 受信データの解析
if ir_data:
    # 最初の信号の時間を基準にする
    start_tick = ir_data[0][1]
    
    # 信号の長さ（マイクロ秒）を計算
    ir_pulses = [(ir_data[i][0], ir_data[i][1] - ir_data[i-1][1]) for i in range(1, len(ir_data))]
    
    print("Received IR signal:")
    for level, duration in ir_pulses:
        print(f"Level: {'High' if level == 1 else 'Low'}, Duration: {duration} µs")
else:
    print("No IR signal received.")
