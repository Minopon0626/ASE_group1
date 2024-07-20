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
        directory_paths.update({
            "Strong_Cooling": os.path.join("Data", "Strong_Cooling"),
            "Strong_Heating": os.path.join("Data", "Strong_Heating")
        })

        for key, path in directory_paths.items():
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"ディレクトリ '{path}' を作成しました。")
            else:
                print(f"ディレクトリ '{path}' は既に存在します。")

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
        final_temperature = None  # 返す温度を保持する変数
        if weather_info is not None:
            print(f"緯度: {lat}, 経度: {lon}")
            print(f"現在の気温: {weather_info['temperature']}°C")
            print(f"天気: {weather_info['weather']}")

            # 手動で部屋の温度を入力
            try:
                room_temperature = float(input("部屋の温度を入力してください (°C): "))
                temperature_diff = abs(room_temperature - weather_info['temperature'])
                print(f"部屋の温度と外気温の差: {temperature_diff}°C")

                if temperature_diff >= 3:
                    if room_temperature > weather_info['temperature'] and room_temperature > cooling_threshold:
                        print("強冷房")
                        read_and_display_file(os.path.join(directory_paths["Strong_Cooling"], "data.txt"))
                        final_temperature = cooling_threshold - 3
                    elif room_temperature < weather_info['temperature'] and room_temperature < heating_threshold:
                        print("強暖房")
                        read_and_display_file(os.path.join(directory_paths["Strong_Heating"], "data.txt"))
                        final_temperature = heating_threshold + 3
                    else:
                        print("強冷房も強暖房も必要ありません")
                        final_temperature = None
                else:
                    if room_temperature > weather_info['temperature']:
                        print(f"部屋の温度 {room_temperature}°C は現在の気温 {weather_info['temperature']}°C より高いです。")
                    elif room_temperature < weather_info['temperature']:
                        print(f"部屋の温度 {room_temperature}°C は現在の気温 {weather_info['temperature']}°C より低いです。")
                    else:
                        print(f"部屋の温度 {room_temperature}°C は現在の気温 {weather_info['temperature']}°C と同じです。")

                    if weather_info['temperature'] >= cooling_threshold:
                        print("冷房")
                        read_and_display_file(os.path.join(directory_paths["Cold"], "data.txt"))
                        final_temperature = cooling_threshold
                    elif weather_info['temperature'] <= heating_threshold:
                        print("暖房")
                        read_and_display_file(os.path.join(directory_paths["Hot"], "data.txt"))
                        final_temperature = heating_threshold
                    else:
                        print("冷房も暖房も必要ありません")
                        final_temperature = None
            except ValueError:
                print("無効な温度が入力されました。")
                final_temperature = None
        else:
            print("気温と天気を取得できませんでした。")
            final_temperature = None

        # 最終的な温度を絶対値で繰り下げ
        if final_temperature is not None:
            final_temperature = int(final_temperature)  # 小数点以下を繰り下げ
        print(f"返却する温度: {final_temperature}°C")
    except ValueError as e:
        print(e)
