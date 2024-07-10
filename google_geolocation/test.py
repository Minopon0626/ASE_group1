"""
ラズベリーパイのWi-Fiアクセスポイント情報を使用して
Google Geolocation APIを通じて位置情報を取得する

使い方:
1. Google Cloud PlatformでAPIキーを取得し, Geolocation APIを有効にする
2. このスクリプト内の `api_key` 変数に取得したAPIキーを設定する
3. スクリプトを実行する
   実行コマンド: sudo python3 test.py
"""

import subprocess  # システムコマンドを実行するためのモジュール
import requests    # HTTPリクエストを送信するためのモジュール
import json        # JSONデータを操作するためのモジュール

# Wi-Fiアクセスポイント情報の取得
def get_wifi_info():
    # 'iwlist'コマンドを使用してWi-Fiスキャンを実行し、結果を取得
    cmd = "sudo iwlist wlan0 scan | grep 'Cell\|ESSID\|Signal level'"
    result = subprocess.check_output(cmd, shell=True).decode('utf-8').split('\n')
    
    wifi_info = []  # Wi-Fi情報を格納するリスト
    
    current_cell = {}  # 現在のアクセスポイント情報を一時的に保持する辞書
    for line in result:
        if 'Cell' in line:
            if current_cell:
                wifi_info.append(current_cell)
            current_cell = {'macAddress': line.split()[4]}
        elif 'ESSID' in line:
            current_cell['ssid'] = line.split(':')[1].strip('"')
        elif 'Signal level' in line:
            current_cell['signalStrength'] = int(line.split('=')[2].split(' ')[0])
    
    # 最後のアクセスポイント情報をリストに追加
    if current_cell:
        wifi_info.append(current_cell)
    
    return wifi_info

# Google Geolocation APIを使用して位置情報を取得
def get_location(wifi_info, api_key):
    url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + api_key
    data = {
        "wifiAccessPoints": wifi_info
    }
    response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    location = response.json()
    return location

if __name__ == "__main__":
    api_key = "YOUR_GOOGLE_API_KEY"  # ここにGoogle APIキーを設定
    wifi_info = get_wifi_info()  # Wi-Fiアクセスポイント情報を取得
    location = get_location(wifi_info, api_key)  # 位置情報を取得
    print(f"Latitude: {location['location']['lat']}, Longitude: {location['location']['lng']}")  # 位置情報を出力
