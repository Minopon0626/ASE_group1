import time  # timeモジュールをインポートして、時間関連の操作を行う
import os  # osモジュールをインポートして、OSとの対話を行う
from capture import photographing  # photographing.pyからcapture_image関数をインポート
from detection import yolo_common  # yolo_common.pyからload_yolo_model関数をインポート
from detection import person_detection  # person_detection.pyからyolo_detect_and_cut_person関数をインポート
from detection import sleeve_detection  # sleeve_detection.pyからyolo_detect_and_cut_sleeve関数をインポート
from file_system import create_or_find_output  # create_or_find_outputモジュールをインポート
from ir import Infrared_rays_send  # Infrared_rays_sendモジュールをインポート
from capture import time_capture  # time_captureモジュールをインポート
import shutil  # shutilモジュールをインポートして、ファイル操作を行う

def main():
    # ディレクトリが存在しない場合は作成
    log_dir = 'log'  # logディレクトリ名
    
    current_dir = '.'
    # outputディレクトリが存在しない場合は作成する
    create_or_find_output.create_or_find_output_dir(current_dir, log_dir)
    # logディレクトリが存在しない場合は作成する

    try:
        # YOLOモデルを初期化
        person_model = yolo_common.load_yolo_model('default_model')  # デフォルトのYOLOモデルをロード
        sleeve_model = yolo_common.load_yolo_model('sleeve_model')  # 半袖と長袖を識別するモデルをロード
    except FileNotFoundError as e:
        print(e)
        return

    while True:  # 無限ループを開始
        # 画像を撮影
        capture_image = photographing.capture_image()
        # capture_image関数を呼び出して、画像を撮影し、ファイル名を取得する
        if capture_image:
            #現在時刻を習得する
            timestamp = time_capture.get_current_timestamp()
            now_dir = create_or_find_output.create_or_find_output_dir(log_dir, timestamp)

            # 撮影した画像をnow_dirにコピー
            shutil.copy(capture_image, now_dir)
            
            # 人物検出を実行し、トリミングした画像をoutputディレクトリに保存
            number_of_people = person_detection.yolo_detect_and_cut_person('captured_image.jpg', now_dir, person_model)
            print(f"検出された人数: {number_of_people}")
            # 検出された人数を出力する

            # もし1人以上の人が検出されたら、半袖と長袖の識別を実行
            if number_of_people > 0:
                sleeve_counts = sleeve_detection.yolo_detect_and_cut_sleeve('captured_image.jpg', now_dir, sleeve_model)
                print(f"半袖: {sleeve_counts.get('short_sleeve', 0)}, 長袖: {sleeve_counts.get('long_sleeve', 0)}")
                
                Infrared_rays_send.send_ir_command()
                # 人が1人以上検出された場合、赤外線コマンドを送信する
        
        # 20秒待機
        time.sleep(20)
        # 20秒待機する

if __name__ == "__main__":
    main()
    # スクリプトが直接実行された場合、main関数を実行する
