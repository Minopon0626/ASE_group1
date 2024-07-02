# pip install Pillow

from PIL import Image
import os

def convert_image_format(input_path, output_path, output_format):
    """
    画像を別の形式に変換します。
    
    Args:
    input_path (str): 入力画像ファイルのパス。
    output_path (str): 変換後の画像ファイルを保存するパス。
    output_format (str): 変換後の画像形式（例：'JPEG', 'PNG', 'BMP'）。
    
    """
    try:
        # 画像を開く
        with Image.open(input_path) as img:
            # 画像を指定された形式で保存する
            img.save(output_path, format=output_format)
        print(f"画像が {output_path} として保存されました")
    except Exception as e:
        print(f"画像の変換中にエラーが発生しました: {e}")

def batch_convert_images(input_directory, output_directory, output_format):
    """
    ディレクトリ内のすべての画像を別の形式に変換します。
    
    Args:
    input_directory (str): 入力画像を含むディレクトリのパス。
    output_directory (str): 変換後の画像を保存するディレクトリのパス。
    output_format (str): 変換後の画像形式（例：'JPEG', 'PNG', 'BMP'）。
    
    """
    # 出力ディレクトリが存在しない場合、作成する
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # 入力ディレクトリ内のすべてのファイルを処理する
    for filename in os.listdir(input_directory):
        # 対応する画像形式のファイルのみを処理する
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff')):
            input_path = os.path.join(input_directory, filename)
            # 出力ファイル名を作成する
            output_filename = os.path.splitext(filename)[0] + '.' + output_format.lower()
            output_path = os.path.join(output_directory, output_filename)
            # 画像形式を変換する
            convert_image_format(input_path, output_path, output_format.upper())

if __name__ == "__main__":
    # プログラムが存在するディレクトリを取得
    base_directory = os.path.dirname(os.path.abspath(__file__))
    # inputとoutputディレクトリのパスを設定
    input_directory = os.path.join(base_directory, 'input')
    output_directory = os.path.join(base_directory, 'output')
    
    # ユーザーから変換後の画像形式を取得
    output_format = input("変換後の画像形式を入力してください (例: 'jpeg', 'png', 'bmp', 'gif', 'tiff'): ").lower()
    
    # 一括変換を実行
    batch_convert_images(input_directory, output_directory, output_format)
