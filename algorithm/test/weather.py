import requests

def get_current_weather(lat, lon, api_key):
    """
    指定された緯度と経度の現在の気温と天気を取得する関数
    :param lat: 緯度
    :param lon: 経度
    :param api_key: 気象APIのキー
    :return: 現在の気温と天気 (dict)
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
        response = requests.get(url)
        weather_data = response.json()
        
        if response.status_code != 200:
            raise Exception(f"APIリクエストに失敗しました: {weather_data}")
        
        weather_info = {
            'temperature': weather_data['main']['temp'],
            'weather': weather_data['weather'][0]['description']
        }
        return weather_info
    
    except Exception as e:
        print(f"エラー: {e}")
        return None
