import Adafruit_DHT  # Adafruit_DHTライブラリをインポート
import RPi.GPIO as GPIO  # RPi.GPIOライブラリをインポート

def main():
    # 温湿度データを取得
    humidity, temperature = Adafruit_DHT.read(sensor, pin)
    if humidity is not None and temperature is not None:
        # データが取得できた場合、それを表示
        print(f"温度: {temperature:.1f}°C 湿度: {humidity:.1f}%")
    else:
        # データが取得できなかった場合、その旨を表示
        print("センサーからデータを取得できませんでした")

if __name__ == "__main__":
    import time  # timeライブラリをインポート

    while True:
        # 温湿度データを取得
        main()
        time.sleep(10)
