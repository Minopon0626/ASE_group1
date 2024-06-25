import os  # osモジュールをインポートして、OSとの対話を行う
import sys  # sysモジュールをインポートして、コマンドライン引数の処理を行う

def find_file_in_current_directory(filename):
    """
    現在のディレクトリおよびサブディレクトリ内で指定されたファイルを検索し、
    存在する場合はその完全パスを返す。

    :param filename: 検索するファイル名
    :return: ファイルの完全パスまたはNone
    """
    current_directory = os.getcwd()
    # os.getcwd()を使用して現在の作業ディレクトリを取得する
    for root, dirs, files in os.walk(current_directory):
        # os.walk()を使用して、ディレクトリツリーを再帰的に歩く
        if filename in files:
            # ファイルリストに指定されたファイル名が存在するか確認する
            return os.path.join(root, filename)
            # ファイルの完全パスを作成し、返す
    return None
    # ファイルが見つからない場合はNoneを返す

if __name__ == "__main__":
    # スクリプトが直接実行された場合に以下のコードを実行する
    if len(sys.argv) != 2:
        # コマンドライン引数の数が正しいか確認する
        print("使い方: python file_path_finder.py <filename>")
        # 正しくない場合、使用方法を示すメッセージを出力する
    else:
        filename = sys.argv[1]
        # コマンドライン引数からファイル名を取得する
        result = find_file_in_current_directory(filename)
        # 指定されたファイル名で検索を実行する
        if result:
            # ファイルが見つかった場合
            print(f"ファイルパス: {result}")
            # ファイルの完全パスを出力する
        else:
            # ファイルが見つからなかった場合
            print("ファイルが見つかりません")
            # ファイルが見つからなかったことを知らせるメッセージを出力する
