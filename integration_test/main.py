import time  # timeモジュールをインポートして、時間関連の操作を行う
import os  # osモジュールをインポートして、OSとの対話を行う
import sys
import cv2

# 'algorithm'ディレクトリをシステムパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'algorithm'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'detection'))

from capture import photographing  # photographing.pyからcapture_image関数をインポート
from detection import yolo_common  # yolo_common.pyからload_yolo_model関数をインポート
from detection import person_detection  # person_detection.pyからyolo_detect_and_cut_person関数をインポート
from detection import sleeve_detection  # sleeve_detection.pyからyolo_detect_and_cut_sleeve関数をインポート
from file_system import create_or_find_output  # create_or_find_outputモジュールをインポート
from ir import Infrared_rays_send  # Infrared_rays_sendモジュールをインポート
from capture import time_capture  # time_captureモジュールをインポート
import shutil  # shutilモジュールをインポートして、ファイル操作を行う
from ASE_group1.integration_test.algorithm import algorithm_main  # algorithm.pyから必要な関数をインポート
from algorithm import file_manager  # ディレクトリ作成とデータ更新関数をインポート

def main():
    # ディレクトリが存在しない場合は作成
    log_dir = 'log'  # logディレクトリ名
    current_dir = '.'
    
    # outputディレクトリが存在しない場合は作成する
    create_or_find_output.create_or_find_output_dir(current_dir, log_dir)
    # logディレクトリが存在しない場合は作成する

    try:
        # YOLOモデルを初期化
        person_model = yolo_common.load_yolo_model('yolov8s')  # デフォルトのYOLOモデルをロード
        sleeve_model = yolo_common.load_yolo_model('best')  # 半袖と長袖を識別するモデルをロード
    except FileNotFoundError as e:
        print(e)
        return

    # 初期位置情報を取得
    location = algorithm_main.get_initial_location()
    # 室内温度のデフォルト値
    room_temperature = 25.0  
    status = 0  # 状態のデフォルト値 (unknown)
    directory_paths = file_manager.create_directories()  # ディレクトリ作成

    while True:  # 無限ループを開始
        # 画像を撮影
        image_data, capture_image_path = photographing.capture_image_data()  # capture_image_data関数を使って画像データを取得
        
        if image_data is not None:
            # 現在時刻を取得する
            timestamp = time_capture.get_current_timestamp()
            now_dir = create_or_find_output.create_or_find_output_dir(log_dir, timestamp)

            # 画像データをnow_dirに保存
            cv2.imwrite(capture_image_path, image_data)  # 画像データをファイルに保存
            
            # 人物検出を実行し、トリミングした画像を取得
            number_of_people, person_images = person_detection.yolo_detect_and_cut_person(image_data, now_dir, person_model)
            print(f"検出された人数: {number_of_people}")

            # もし1人以上の人が検出されたら、半袖と長袖の識別を実行
            if number_of_people > 0:
                time.sleep(4)
                short_sleeve_count = 0
                long_sleeve_count = 0
                unknown_count = 0
                for person_image_path in person_images:
                    # 画像データを読み込む
                    person_image = cv2.imread(person_image_path)
                    detected_sleeve = sleeve_detection.yolo_detect_and_cut_sleeve(person_image, now_dir, sleeve_model)
                    print(f"人物 {person_images.index(person_image_path) + 1} の識別結果: {detected_sleeve}")  # デバッグ用に識別結果を表示
                    if detected_sleeve == "hansode":
                        short_sleeve_count += 1
                        print(f"人物 {person_images.index(person_image_path) + 1}: 半袖")
                    elif detected_sleeve == "nagasode":
                        long_sleeve_count += 1
                        print(f"人物 {person_images.index(person_image_path) + 1}: 長袖")
                    else:
                        unknown_count += 1
                        print(f"人物 {person_images.index(person_image_path) + 1}: 不明")
                
                print(f"総計 - 半袖: {short_sleeve_count}, 長袖: {long_sleeve_count}, 不明: {unknown_count}")
                
                cooling_threshold, heating_threshold, status = algorithm_main.process_data(room_temperature, number_of_people, long_sleeve_count, short_sleeve_count, status, location, directory_paths)
                
                if cooling_threshold is not None and heating_threshold is not None:
                    file_manager.update_data_file(room_temperature, cooling_threshold, heating_threshold, status, number_of_people, directory_paths)
                
                Infrared_rays_send.send_ir_command()
                # 人が1人以上検出された場合、赤外線コマンドを送信する
        
        # 20秒待機
        time.sleep(20)
        # 20秒待機する

if __name__ == "__main__":
    main()
    # スクリプトが直接実行された場合、main関数を実行する
