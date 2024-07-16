import os  # osモジュールをインポートして、OSとの対話を行う

def create_or_find_output_dir(base_directory='.', directory='output'):
    """
    指定されたディレクトリが存在しない場合は作成し、
    存在する場合はその完全パスを返す。また、指定されたベースディレクトリの
    サブディレクトリを検索してディレクトリを作成する。

    Parameters:
    base_directory (str): 基本ディレクトリ (デフォルトは現在のディレクトリ)
    directory (str): ディレクトリ名 (デフォルトは 'output')

    Returns:
    str: ディレクトリの完全パス
    """
    
    def find_dir(base, dir_name):
        """
        基本ディレクトリ内で指定された名前のディレクトリを検索する。

        Parameters:
        base (str): 検索を開始する基本ディレクトリ
        dir_name (str): 検索するディレクトリ名

        Returns:
        str: 見つかったディレクトリの完全パス、見つからなければNone
        """
        # os.walkを使用してディレクトリツリーを歩く
        for root, dirs, files in os.walk(base):
            # 現在のディレクトリ名がdir_nameと一致するかを確認
            if os.path.basename(root) == dir_name:
                return root  # 一致する場合、そのディレクトリのパスを返す
        return None  # 一致するディレクトリが見つからなければNoneを返す

    # base_directoryが'.'の場合
    if base_directory == '.':
        target_directory = os.path.abspath(directory)  # 指定されたディレクトリの絶対パスを取得
    else:
        # base_directoryが'.'以外の場合
        base_path = find_dir('.', base_directory)  # 基本ディレクトリを検索
        if not base_path:
            # 指定されたディレクトリが見つからない場合は例外を発生
            raise FileNotFoundError(f"'{base_directory}' ディレクトリが見つかりません。")
        # 見つかった基本ディレクトリ内に新しいディレクトリのパスを生成
        target_directory = os.path.abspath(os.path.join(base_path, directory))
    
    # 指定されたディレクトリが存在しない場合は作成
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)  # 新しいディレクトリを作成
        print(f"'{target_directory}' ディレクトリを作成しました。")  # 作成したことを出力
    else:
        print(f"'{target_directory}' ディレクトリは既に存在します。")  # 既に存在することを出力

    return target_directory  # ディレクトリの完全パスを返す

# 使用例（この部分は他のプログラムでimportする場合には不要）
if __name__ == "__main__":
    print(create_or_find_output_dir('.', 'output'))
    print(create_or_find_output_dir('existing_base_directory', 'output'))
