from geolocation import get_wifi_info, get_location
from weather import get_current_weather

if __name__ == "__main__":
    google_api_key = "AIzaSyCGqNUFFIdsC9ZwABMIRVNmdmGfwILjODU"  # ここにGoogle APIキーを設定
    weather_api_key = "69c99674130d87692972008a78fff1e0"  # ここにOpenWeatherMap APIキーを設定
    
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
    else:
        print("気温と天気を取得できませんでした。")
