import time  # timeモジュールをインポートして、時間関連の操作を行う
import os  # osモジュールをインポートして、OSとの対話を行う
from photographing import capture_image  # capturing.pyからcapture_image関数をインポート
from ImageDetection import yolo_detect_and_cut  # ImageDetection.pyからyolo_detect_and_cut関数をインポート
import create_or_find_output  # create_or_find_outputモジュールをインポート
import Infrared_rays_send  # Infrared_rays_sendモジュールをインポート
import time_capture

def main():
    # ディレクトリが存在しない場合は作成
    capture_dir = 'capture'  # 画像を保存するためのディレクトリ名
    output_dir = 'output'  # 処理された画像を保存するためのディレクトリ名
    
    log_dir = 'log'
    
    current_dir = '.'
    create_or_find_output.create_or_find_output_dir(current_dir, capture_dir)
    # captureディレクトリが存在しない場合は作成する
    create_or_find_output.create_or_find_output_dir(current_dir, output_dir)
    # outputディレクトリが存在しない場合は作成する

    create_or_find_output.create_or_find_output_dir(current_dir, log_dir)
    
    while True:  # 無限ループを開始
        # 画像を撮影
        image_name = capture_image()
        # capture_image関数を呼び出して、画像を撮影し、ファイル名を取得する
        if image_name:

            timestamp = time_capture.get_current_timestamp()
            # 撮影した画像をcaptureディレクトリに移動

            captured_image_path = os.path.join(capture_dir, image_name)
            now_dir = create_or_find_output.create_or_find_output_dir(log_dir, timestamp)

            # 画像の新しいパスを作成する
            # os.rename(image_name, captured_image_path)
            # (コメントアウトされているが) 画像を新しいパスに移動する
            
            # YOLO検出を実行し、トリミングした画像をoutputディレクトリに保存
            number_of_people = yolo_detect_and_cut('captured_image.jpg')
            # yolo_detect_and_cut関数を呼び出して、人数を検出し、トリミングした画像を保存する
            print(f"検出された人数: {number_of_people}")
            # 検出された人数を出力する

            # もし1人以上の人が検出されたらIRコマンドを送信
            if number_of_people > 0:
                Infrared_rays_send.send_ir_command()
                # 人が1人以上検出された場合、赤外線コマンドを送信する
        
        # 20秒待機
        time.sleep(20)
        # 20秒待機する

if __name__ == "__main__":
    main()
    # スクリプトが直接実行された場合、main関数を実行する
