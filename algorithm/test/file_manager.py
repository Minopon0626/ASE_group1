import os  # ファイルやディレクトリの操作を行うための標準ライブラリ

def create_directories():
    base_dir = "Data"  # データを保存するベースディレクトリ名
    hot_dir = os.path.join(base_dir, "Hot")  # 暖房用データを保存するディレクトリのパス
    cold_dir = os.path.join(base_dir, "Cold")  # 冷房用データを保存するディレクトリのパス

    directories = {
        "Hot": hot_dir,  # ディレクトリ辞書に暖房用ディレクトリを追加
        "Cold": cold_dir  # ディレクトリ辞書に冷房用ディレクトリを追加
    }

    # 暖房用ディレクトリが存在しない場合は作成
    if not os.path.exists(hot_dir):
        os.makedirs(hot_dir)
        print(f"ディレクトリ '{hot_dir}' を作成しました。")
    else:
        print(f"ディレクトリ '{hot_dir}' は既に存在します。")

    # 冷房用ディレクトリが存在しない場合は作成
    if not os.path.exists(cold_dir):
        os.makedirs(cold_dir)
        print(f"ディレクトリ '{cold_dir}' を作成しました。")
    else:
        print(f"ディレクトリ '{cold_dir}' は既に存在します。")

    return directories  # ディレクトリパスの辞書を返す

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

def update_data_file(room_temperature, cooling_threshold, heating_threshold, status, num_people, directory_paths):
    # 室温が冷房の基準温度以上の場合
    if room_temperature >= cooling_threshold:
        file_path = os.path.join(directory_paths["Cold"], "data.txt")  # 冷房用データファイルのパス
        setting_temperature = cooling_threshold  # 設定温度を冷房の基準温度に設定
    # 室温が暖房の基準温度以下の場合
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
