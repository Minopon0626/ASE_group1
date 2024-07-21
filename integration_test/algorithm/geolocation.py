# geolocation.py
import subprocess  # システムコマンドを実行するためのモジュール
import requests    # HTTPリクエストを送信するためのモジュール
import json        # JSONデータを操作するためのモジュール
import platform    # プラットフォーム情報を取得するためのモジュール
import sys         # システム固有のパラメータや関数にアクセスするためのモジュール
import chardet     # エンコーディングを自動検出するためのモジュール
import re          # 正規表現モジュール

# MACアドレスのフォーマットを検証および修正する関数
def format_mac_address(mac):
    mac = mac.lower().replace('-', ':')
    if re.match("[0-9a-f]{2}([:-][0-9a-f]{2}){5}$", mac):
        return mac
    else:
        raise ValueError(f"無効なMACアドレス形式: {mac}")

# Wi-Fiアクセスポイント情報の取得
def get_wifi_info():
    os_name = platform.system()
    if os_name == "Linux":
        cmd = r"sudo iwlist wlan0 scan | grep -E 'Cell|ESSID|Signal level'"
    elif os_name == "Windows":
        cmd = "netsh wlan show networks mode=bssid"
    else:
        raise NotImplementedError(f"OS {os_name} はサポートされていません")

    try:
        result = subprocess.check_output(cmd, shell=True)
        encoding = chardet.detect(result)['encoding']
        result = result.decode(encoding).split('\n')
    except subprocess.CalledProcessError as e:
        print(f"コマンド '{cmd}' は終了ステータス {e.returncode} を返しました")
        sys.exit(1)
    except FileNotFoundError:
        print("無線ネットワークが見つかりません。無線接続を確認してください。")
        sys.exit(1)

    wifi_info = []  # Wi-Fi情報を格納するリスト

    current_cell = {}  # 現在のアクセスポイント情報を一時的に保持する辞書
    for line in result:
        if os_name == "Linux" and 'Cell' in line:
            if current_cell:
                wifi_info.append(current_cell)
            current_cell = {'macAddress': format_mac_address(line.split()[4])}
        elif os_name == "Windows" and 'BSSID' in line:
            if current_cell:
                wifi_info.append(current_cell)
            mac_address = line.split(':', 1)[1].strip()
            current_cell = {'macAddress': format_mac_address(mac_address)}
        elif 'ESSID' in line:
            current_cell['ssid'] = line.split(':', 1)[1].strip().strip('"')
        elif 'Signal level' in line or 'Signal' in line:
            if os_name == "Linux":
                signal_strength = line.split('=')[-1].split(' ')[0]
                if 'dBm' in signal_strength:
                    current_cell['signalStrength'] = int(signal_strength.replace('dBm', '').strip())
            elif os_name == "Windows":
                current_cell['signalStrength'] = int(line.split(':', 1)[1].strip().replace('%', ''))

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
    
    if "location" not in location:
        print("エラーが発生しました: ", location)
        sys.exit(1)
    
    return location

if __name__ == "__main__":
    api_key = "YOUR_GOOGLE_API_KEY"  # ここにGoogle APIキーを設定
    wifi_info = get_wifi_info()  # Wi-Fiアクセスポイント情報を取得
    if not wifi_info:
        print("Wi-Fiアクセスポイント情報が取得できませんでした。")
        sys.exit(1)
    location = get_location(wifi_info, api_key)  # 位置情報を取得
    print(f"緯度: {location['location']['lat']}, 経度: {location['location']['lng']}")  # 位置情報を出力
