import time
import os
from photographing import capture_image
from ImageDetection import yolo_detect_and_cut
import create_or_find_output
import Infrared_rays_send

def main():
    # ディレクトリが存在しない場合は作成
    capture_dir = 'capture'
    output_dir = 'output'
    create_or_find_output.create_or_find_output_dir(capture_dir)
    create_or_find_output.create_or_find_output_dir(output_dir)
    
    while True:
        # 画像を撮影
        image_name = capture_image()
        if image_name:
            # 撮影した画像をcaptureディレクトリに移動
            captured_image_path = os.path.join(capture_dir, image_name)
            # os.rename(image_name, captured_image_path)
            
            # YOLO検出を実行し、トリミングした画像をoutputディレクトリに保存
            number_of_people = yolo_detect_and_cut("captured_image.jpg")
            print(f"検出された人数: {number_of_people}")

            # もし1人以上の人が検出されたらIRコマンドを送信
            if number_of_people > 0:
                Infrared_rays_send.send_ir_command()
        
        # 20秒待機
        time.sleep(20)

if __name__ == "__main__":
    main()
