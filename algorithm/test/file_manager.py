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
