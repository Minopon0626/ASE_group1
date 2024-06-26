import pigpio
import time
import threading

# GPIOピンの設定
IR_PIN = 17

class IRReceiver(threading.Thread):
    def __init__(self, pi, pin):
        threading.Thread.__init__(self)
        self.pi = pi
        self.pin = pin
        self.pulse_widths = []
        self.last_tick = None
        self.running = True

        self.pi.set_mode(self.pin, pigpio.INPUT)
        self.cb = self.pi.callback(self.pin, pigpio.FALLING_EDGE, self._callback)

    def _callback(self, gpio, level, tick):
        if self.last_tick is not None:
            pulse_width = pigpio.tickDiff(self.last_tick, tick)
            self.pulse_widths.append(pulse_width)

        self.last_tick = tick

    def run(self):
        while self.running:
            time.sleep(0.001)  # 短いスリープ時間

    def stop(self):
        self.running = False
        self.cb.cancel()

# pigpioの初期化
pi = pigpio.pi()

if not pi.connected:
    exit()

# IRReceiverスレッドの初期化と開始
ir_receiver = IRReceiver(pi, IR_PIN)
ir_receiver.start()

# メインスレッドでの非ブロッキングな待機
print("リモコンのボタンを押してください...")
start_time = time.time()
capture_duration = 5  # 信号をキャプチャする時間（秒）

# 非ブロッキングで指定時間待機
while time.time() - start_time < capture_duration:
    time.sleep(0.01)  # メインスレッドでの短いスリープ

# IRReceiverスレッドの停止
ir_receiver.stop()
ir_receiver.join()

# 計測結果を表示する
pi.stop()

if ir_receiver.pulse_widths:
    average_pulse_width = sum(ir_receiver.pulse_widths) / len(ir_receiver.pulse_widths)
    frequency = 1 / (average_pulse_width / 1e6)
    print(f"平均パルス幅: {average_pulse_width:.2f} us")
    print(f"推定キャリア周波数: {frequency:.2f} Hz")
else:
    print("パルス幅が測定できませんでした。")
