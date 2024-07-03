# pip install pillow

# python size_down.py input.jpg output.jpg 100 100

from PIL import Image
import argparse

def lower_image_resolution(input_path, output_path, new_width, new_height):
    """
    指定した画像の解像度を低くする関数。
    
    Parameters:
    input_path (str): 入力画像のファイルパス。
    output_path (str): 出力画像のファイルパス。
    new_width (int): リサイズ後の幅。
    new_height (int): リサイズ後の高さ。
    """
    # 画像を開く
    img = Image.open(input_path)
    
    # 画像のアスペクト比を維持するためのリサイズ
    img.thumbnail((new_width, new_height), Image.Resampling.LANCZOS)
    
    # リサイズした画像を保存
    img.save(output_path)
    
    print(f"画像は {output_path} に保存されました。解像度: {img.width}x{img.height}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="画像の解像度を低くするプログラム。")
    parser.add_argument("input_path", help="入力画像ファイルのパス。")
    parser.add_argument("output_path", help="出力画像ファイルの保存先パス。")
    parser.add_argument("new_width", type=int, help="画像の新しい幅。")
    parser.add_argument("new_height", type=int, help="画像の新しい高さ。")
    
    args = parser.parse_args()
    
    lower_image_resolution(args.input_path, args.output_path, args.new_width, args.new_height)
