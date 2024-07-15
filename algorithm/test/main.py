from geolocation import get_wifi_info, get_location
from weather import get_current_weather
from file_manager import create_directories, read_data_file, read_and_display_file
from temperature_calculator import calculate_temperature, validate_thresholds
import sys
import os

if __name__ == "__main__":
    google_api_key = "AIzaSyCGqNUFFIdsC9ZwABMIRVNmdmGfwILjODU"  # ここにGoogle APIキーを設定
    weather_api_key = "69c99674130d87692972008a78fff1e0"  # ここにOpenWeatherMap APIキーを設定

    try:
        # ディレクトリ作成とパスの辞書を取得
        directory_paths = create_directories()

        # 各ディレクトリのデータを読み取る
        cold_data = read_data_file(os.path.join(directory_paths["Cold"], "data.txt"))
        hot_data = read_data_file(os.path.join(directory_paths["Hot"], "data.txt"))

        print(f"Cold data: {cold_data}")  # デバッグメッセージ
        print(f"Hot data: {hot_data}")    # デバッグメッセージ

        # 冷房と暖房の設定温度を計算
        cooling_threshold = calculate_temperature(cold_data, 'cooling')
        heating_threshold = calculate_temperature(hot_data, 'heating')

        # 計算された温度を表示
        if cooling_threshold is not None:
            print(f"計算された冷房の基準温度: {cooling_threshold}°C")
        else:
            print("冷房の基準温度を計算できませんでした。")

        if heating_threshold is not None:
            print(f"計算された暖房の基準温度: {heating_threshold}°C")
        else:
            print("暖房の基準温度を計算できませんでした。")

        # 定数として設定された冷房と暖房の基準温度を検証
        validate_thresholds(cooling_threshold, heating_threshold)

        wifi_info = get_wifi_info()  # Wi-Fiアクセスポイント情報を取得
        if not wifi_info:
            print("Wi-Fiアクセスポイント情報が取得できませんでした。")
            sys.exit(1)

        location = get_location(wifi_info, google_api_key)  # 位置情報を取得
        lat = location['location']['lat']
        lon = location['location']['lng']

        weather_info = get_current_weather(lat, lon, weather_api_key)
        if weather_info is not None:
            print(f"緯度: {lat}, 経度: {lon}")
            print(f"現在の気温: {weather_info['temperature']}°C")
            print(f"天気: {weather_info['weather']}")

            # 外気温が冷房の基準温度以上か暖房の基準温度以下かを確認して該当ファイルを表示
            if weather_info['temperature'] >= cooling_threshold:
                print("冷房")
                read_and_display_file(os.path.join(directory_paths["Cold"], "data.txt"))
            elif weather_info['temperature'] <= heating_threshold:
                print("暖房")
                read_and_display_file(os.path.join(directory_paths["Hot"], "data.txt"))
            else:
                print("冷房も暖房も必要ありません")

            # 手動で部屋の温度を入力
            try:
                room_temperature = float(input("部屋の温度を入力してください (°C): "))
                if room_temperature > weather_info['temperature']:
                    print(f"部屋の温度 {room_temperature}°C は現在の気温 {weather_info['temperature']}°C より高いです。")
                elif room_temperature < weather_info['temperature']:
                    print(f"部屋の温度 {room_temperature}°C は現在の気温 {weather_info['temperature']}°C より低いです。")
                else:
                    print(f"部屋の温度 {room_temperature}°C は現在の気温 {weather_info['temperature']}°C と同じです。")
            except ValueError:
                print("無効な温度が入力されました。")
        else:
            print("気温と天気を取得できませんでした。")
    except ValueError as e:
        print(e)
