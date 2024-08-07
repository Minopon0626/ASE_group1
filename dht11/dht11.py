import Adafruit_DHT  # Adafruit_DHTライブラリをインポート
import RPi.GPIO as GPIO  # RPi.GPIOライブラリをインポート

# センサーのタイプを定義（DHT11）
sensor = Adafruit_DHT.DHT11

# センサーのデータピンのGPIO番号を定義
pin = 4  # 例: GPIO4

# GPIOの初期化
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

def read_dht11():
    """
    DHT11センサーから温湿度データを取得する関数
    
    戻り値:
        tuple: (温度, 湿度) 温湿度データが取得できない場合は (None, None)
    """
    # 温湿度データを取得
    humidity, temperature = Adafruit_DHT.read(sensor, pin)
    if humidity is not None and temperature is not None:
        # 温度と湿度が取得できた場合、それらを返す
        return temperature, humidity
    else:
        # データが取得できなかった場合、(None, None)を返す
        return None, None

if __name__ == "__main__":
    import time  # timeライブラリをインポート

    while True:
        # 温湿度データを取得
        temperature, humidity = read_dht11()
        if humidity is not None and temperature is not None:
            # データが取得できた場合、それを表示
            print(f"温度: {temperature:.1f}°C 湿度: {humidity:.1f}%")
        else:
            # データが取得できなかった場合、その旨を表示
            print("センサーからデータを取得できませんでした")
        # 10秒ごとにデータを取得
        time.sleep(10)
