from geolocation import get_wifi_info, get_location  # 位置情報を取得する関数をインポート
from weather import get_current_weather  # 天気情報を取得する関数をインポート
from temperature_calculator import calculate_temperature, validate_thresholds, adjust_temperature_for_people, calculate_person_adjustment, adjust_person_count  # 温度計算関数をインポート
from file_manager import read_data_file, read_and_display_file
import sys  # システム関連の機能を提供する標準ライブラリ
import os  # ファイルやディレクトリの操作を行うための標準ライブラリ

def get_initial_location():
    google_api_key = "AIzaSyCGqNUFFIdsC9ZwABMIRVNmdmGfwILjODU"  # Google APIキーを設定
    wifi_info = get_wifi_info()  # Wi-Fiアクセスポイント情報を取得
    if not wifi_info:
        print("Wi-Fiアクセスポイント情報が取得できませんでした。")  # Wi-Fi情報が取得できない場合のエラーメッセージ
        sys.exit(1)  # プログラムを終了

    location = get_location(wifi_info, google_api_key)  # 位置情報を取得
    return location  # 位置情報を返す

def process_data(room_temperature, num_people, long_sleeve_count, short_sleeve_count, status, location, directory_paths):
    weather_api_key = "69c99674130d87692972008a78fff1e0"  # OpenWeatherMap APIキーを設定
    long_sleeve_rate = 1.0  # 長袖の温度変化率を設定
    short_sleeve_rate = 0.5  # 半袖の温度変化率を設定

    try:
        # 各ディレクトリのデータを読み取る
        cold_data = read_data_file(os.path.join(directory_paths["Cold"], "data.txt"))
        hot_data = read_data_file(os.path.join(directory_paths["Hot"], "data.txt"))

        print(f"Cold data: {cold_data}")  # デバッグメッセージ：冷房データを表示
        print(f"Hot data: {hot_data}")    # デバッグメッセージ：暖房データを表示

        # 冷房と暖房の設定温度を計算
        cooling_threshold = calculate_temperature(cold_data, 'cooling')
        heating_threshold = calculate_temperature(hot_data, 'heating')

        # 人数確認と調整
        long_sleeve_count, short_sleeve_count = adjust_person_count(num_people, long_sleeve_count, short_sleeve_count)

        # 人数補正量を計算
        person_adjustment = calculate_person_adjustment(long_sleeve_count, short_sleeve_count, long_sleeve_rate, short_sleeve_rate)

        # 人数補正量に応じて冷房と暖房の基準温度を調整
        if cooling_threshold is not None and heating_threshold is not None:
            cooling_threshold, heating_threshold = adjust_temperature_for_people(cooling_threshold, heating_threshold, person_adjustment)
            print(f"人数補正後の冷房の基準温度: {cooling_threshold}°C")
            print(f"人数補正後の暖房の基準温度: {heating_threshold}°C")
        else:
            print("冷房または暖房の基準温度を計算できませんでした。")

        # 定数として設定された冷房と暖房の基準温度を検証
        validate_thresholds(cooling_threshold, heating_threshold)

        lat = location['location']['lat']  # 緯度を取得
        lon = location['location']['lng']  # 経度を取得

        weather_info = get_current_weather(lat, lon, weather_api_key)  # 現在の天気情報を取得
        if weather_info is not None:
            print(f"緯度: {lat}, 経度: {lon}")  # 取得した緯度経度を表示
            print(f"現在の気温: {weather_info['temperature']}°C")  # 現在の気温を表示
            print(f"天気: {weather_info['weather']}")  # 現在の天気を表示

            # 外気温が冷房の基準温度以上か暖房の基準温度以下かを確認して該当ファイルを表示
            if weather_info['temperature'] >= cooling_threshold:
                print("冷房")
                read_and_display_file(os.path.join(directory_paths["Cold"], "data.txt"))
            elif weather_info['temperature'] <= heating_threshold:
                print("暖房")
                read_and_display_file(os.path.join(directory_paths["Hot"], "data.txt"))
            else:
                print("冷房も暖房も必要ありません")

            # 部屋の温度を表示
            if room_temperature > weather_info['temperature']:
                print(f"部屋の温度 {room_temperature}°C は現在の気温 {weather_info['temperature']}°C より高いです。")
                status = 1  # 部屋が外より熱い
            elif room_temperature < weather_info['temperature']:
                print(f"部屋の温度 {room_temperature}°C は現在の気温 {weather_info['temperature']}°C より低いです。")
                status = 2  # 部屋が外より寒い
            else:
                print(f"部屋の温度 {room_temperature}°C は現在の気温 {weather_info['temperature']}°C と同じです。")
                status = 0  # 部屋と外が同じ温度とする (unknown)

        else:
            print("気温と天気を取得できませんでした。")
            status = 0  # デフォルトの状態を unknown とする

        return cooling_threshold, heating_threshold, status

    except ValueError as e:
        print(e)
        return None, None, status
