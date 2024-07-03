# pip install pillow


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
    img.thumbnail((new_width, new_height), Image.ANTIALIAS)
    
    # リサイズした画像を保存
    img.save(output_path)
    
    print(f"Image saved at {output_path} with resolution {img.width}x{img.height}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reduce the resolution of an image.")
    parser.add_argument("input_path", help="Path to the input image file.")
    parser.add_argument("output_path", help="Path to save the output image file.")
    parser.add_argument("new_width", type=int, help="New width of the image.")
    parser.add_argument("new_height", type=int, help="New height of the image.")
    
    args = parser.parse_args()
    
    lower_image_resolution(args.input_path, args.output_path, args.new_width, args.new_height)
