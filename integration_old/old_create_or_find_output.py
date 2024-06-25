import os  # osモジュールをインポートして、OSとの対話を行う

def create_or_find_output_dir(directory='output'):
    """
    指定されたディレクトリが存在しない場合は作成し、
    存在する場合はその完全パスを返す。

    Parameters:
    directory (str): ディレクトリ名 (デフォルトは 'output')

    Returns:
    str: ディレクトリの完全パス
    """
    # ディレクトリが存在するか確認
    if not os.path.exists(directory):
        # os.path.existsは指定したパスが存在するかどうかを確認する

        # 存在しない場合は作成
        os.makedirs(directory)
        # os.makedirsは指定したディレクトリを作成する
        print(f"'{directory}' ディレクトリを作成しました。")
        # ディレクトリを作成したことを知らせるメッセージを出力する
    else:
        print(f"'{directory}' ディレクトリは既に存在します。")
        # ディレクトリが既に存在することを知らせるメッセージを出力する

    # ディレクトリの完全パスを取得
    full_path = os.path.abspath(directory)
    # os.path.abspathは指定したパスの絶対パスを返す

    return full_path
    # 絶対パスを返す
