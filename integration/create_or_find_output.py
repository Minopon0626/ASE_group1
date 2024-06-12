import os

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
        # 存在しない場合は作成
        os.makedirs(directory)
        print(f"'{directory}' ディレクトリを作成しました。")
    else:
        print(f"'{directory}' ディレクトリは既に存在します。")

    # ディレクトリの完全パスを取得
    full_path = os.path.abspath(directory)
    return full_path
