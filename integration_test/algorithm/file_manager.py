import os  # ファイルやディレクトリの操作を行うための標準ライブラリ

def create_directories():
    # 現在のディレクトリパスを取得
    current_dir = os.path.dirname(__file__)
    
    # ディレクトリパスを作成
    cold_dir = os.path.join(current_dir, 'Cold')
    hot_dir = os.path.join(current_dir, 'Hot')
    
    # ディレクトリが存在しない場合は作成
    if not os.path.exists(cold_dir):
        os.makedirs(cold_dir)
    if not os.path.exists(hot_dir):
        os.makedirs(hot_dir)
    
    # ディレクトリパスを辞書として返す
    return {
        "Cold": cold_dir,
        "Hot": hot_dir
    }

def read_data_file(file_path):
    data = []  # データを格納するリスト
    # ファイルを読み取りモードで開く
    with open(file_path, 'r') as file:
        # 各行を読み取り、リストに追加
        for line in file.readlines():
            data.append(line.strip())
    return data  # 読み取ったデータを返す

def read_and_display_file(file_path):
    # ファイルを読み取りモードで開く
    with open(file_path, 'r') as file:
        content = file.read()  # ファイル内容を読み取る
    print(f"{file_path} の内容:\n{content}")  # ファイル内容を表示する

def determine_status(room_temperature, cooling_threshold, heating_threshold):
    # 室温が冷房の基準温度以上の場合
    if room_temperature >= cooling_threshold:
        if abs(room_temperature - cooling_threshold) <= 3:
            return 2  # 寒い
        else:
            return 1  # 熱い
    # 室温が暖房の基準温度以下の場合
    elif room_temperature <= heating_threshold:
        if abs(room_temperature - heating_threshold) <= 3:
            return 2  # 寒い
        else:
            return 1  # 熱い
    # 上記以外の場合は既存の状態を維持
    return 0  # unknown

def update_data_file(room_temperature, cooling_threshold, heating_threshold, status, num_people, directory_paths):
    # 状態が unknown (0) の場合、新しい状態を決定
    if status == 0:
        status = determine_status(room_temperature, cooling_threshold, heating_threshold)

    # データを書き込むファイルのパスを決定
    if room_temperature >= cooling_threshold:
        file_path = os.path.join(directory_paths["Cold"], "data.txt")  # 冷房用データファイルのパス
        setting_temperature = cooling_threshold  # 設定温度を冷房の基準温度に設定
    elif room_temperature <= heating_threshold:
        file_path = os.path.join(directory_paths["Hot"], "data.txt")  # 暖房用データファイルのパス
        setting_temperature = heating_threshold  # 設定温度を暖房の基準温度に設定
    else:
        # 室温が冷房と暖房の間の場合、最も近い方の閾値を使用
        if abs(room_temperature - cooling_threshold) < abs(room_temperature - heating_threshold):
            file_path = os.path.join(directory_paths["Cold"], "data.txt")  # 冷房用データファイルのパス
            setting_temperature = cooling_threshold  # 設定温度を冷房の基準温度に設定
        else:
            file_path = os.path.join(directory_paths["Hot"], "data.txt")  # 暖房用データファイルのパス
            setting_temperature = heating_threshold  # 設定温度を暖房の基準温度に設定

    # 書き込むデータを文字列形式で作成
    data_to_write = f"{room_temperature},{status},{num_people},{setting_temperature}\n"
    print(f"書き込むデータ: {data_to_write.strip()}")  # 書き込むデータを表示

    # データをファイルに追加書き込みモードで開き、書き込む
    with open(file_path, 'a') as file:
        file.write(data_to_write)
    print(f"Updated data has been saved to {file_path}")  # データが保存されたことを表示
    print(f"ログ: 室温 {room_temperature}°C, 状態 {status}, 人数 {num_people}, 設定温度 {setting_temperature} を {file_path} に書き込みました。")  # 書き込み内容のログを表示