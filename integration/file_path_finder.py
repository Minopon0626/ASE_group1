import os
import sys

def find_file_in_current_directory(filename):
    """
    現在のディレクトリおよびサブディレクトリ内で指定されたファイルを検索し、
    存在する場合はその完全パスを返す。

    :param filename: 検索するファイル名
    :return: ファイルの完全パスまたはNone
    """
    current_directory = os.getcwd()
    for root, dirs, files in os.walk(current_directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使い方: python file_path_finder.py <filename>")
    else:
        filename = sys.argv[1]
        result = find_file_in_current_directory(filename)
        if result:
            print(f"ファイルパス: {result}")
        else:
            print("ファイルが見つかりません")
