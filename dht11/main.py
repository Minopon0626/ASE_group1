from dht11 import read_dht11  # dht11モジュールからread_dht11関数をインポート

def main():
    # 温湿度データを取得
    temperature, humidity = read_dht11()
    if humidity is not None and temperature is not None:
        # データが取得できた場合、それを表示
        print(f"温度: {temperature:.1f}°C 湿度: {humidity:.1f}%")
    else:
        # データが取得できなかった場合、その旨を表示
        print("センサーからデータを取得できませんでした")

if __name__ == "__main__":
    main()  # main関数を実行
