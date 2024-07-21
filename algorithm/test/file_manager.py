import os

def create_directories():
    base_dir = "Data"
    hot_dir = os.path.join(base_dir, "Hot")
    cold_dir = os.path.join(base_dir, "Cold")

    directories = {
        "Hot": hot_dir,
        "Cold": cold_dir
    }

    if not os.path.exists(hot_dir):
        os.makedirs(hot_dir)
        print(f"ディレクトリ '{hot_dir}' を作成しました。")
    else:
        print(f"ディレクトリ '{hot_dir}' は既に存在します。")

    if not os.path.exists(cold_dir):
        os.makedirs(cold_dir)
        print(f"ディレクトリ '{cold_dir}' を作成しました。")
    else:
        print(f"ディレクトリ '{cold_dir}' は既に存在します。")

    return directories

def read_data_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            data.append(line.strip())
    return data

def read_and_display_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    print(f"{file_path} の内容:\n{content}")

def update_data_file(room_temperature, cooling_threshold, heating_threshold, status, num_people, directory_paths):
    if room_temperature >= cooling_threshold:
        file_path = os.path.join(directory_paths["Cold"], "data.txt")
        setting_temperature = cooling_threshold
    elif room_temperature <= heating_threshold:
        file_path = os.path.join(directory_paths["Hot"], "data.txt")
        setting_temperature = heating_threshold
    else:
        # 冷房と暖房の間の温度ならば、最も近い方の閾値を使用
        if abs(room_temperature - cooling_threshold) < abs(room_temperature - heating_threshold):
            file_path = os.path.join(directory_paths["Cold"], "data.txt")
            setting_temperature = cooling_threshold
        else:
            file_path = os.path.join(directory_paths["Hot"], "data.txt")
            setting_temperature = heating_threshold

    data_to_write = f"{room_temperature},{status},{num_people},{setting_temperature}\n"
    print(f"書き込むデータ: {data_to_write.strip()}")

    with open(file_path, 'a') as file:
        file.write(data_to_write)
    print(f"Updated data has been saved to {file_path}")
    print(f"ログ: 室温 {room_temperature}°C, 状態 {status}, 人数 {num_people}, 設定温度 {setting_temperature} を {file_path} に書き込みました。")
