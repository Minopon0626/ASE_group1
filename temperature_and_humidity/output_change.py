import RPi.GPIO as GPIO
import dht11
import time
import datetime
from custom_print import start_cutom_print, custom_print

# GPIOの初期化
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# DHT11の設定
instance = dht11.DHT11(pin=5)

def read_dht11():
    result = instance.read()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if result.is_valid():
        return f"温度: {result.temperature:.1f}C", f"湿度: {result.humidity:.1f}%", f"現在の時間: {current_time}"
    else:
        return "データの取得に失敗しました", "", f"現在の時間: {current_time}"

if __name__ == "__main__":
    start_cutom_print()
    try:
        while True:
            line1, line2, line3 = read_dht11()
            custom_print(line1, line2, line3)
            time.sleep(6)  # 6秒ごとにデータを取得
    except KeyboardInterrupt:
        print("クリーンアップ中")
        GPIO.cleanup()
