import time  # timeモジュールをインポートして、時間関連の操作を行う
import os  # osモジュールをインポートして、OSとの対話を行う
import sys
import cv2
import threading
import queue

# 'algorithm'ディレクトリをシステムパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'algorithm'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'detection'))

from pushbutton import setup_gpio, handle_switches, shared_queue
from capture import photographing  # photographing.pyからcapture_image関数をインポート
from detection import yolo_common  # yolo_common.pyからload_yolo_model関数をインポート
from detection import person_detection  # person_detection.pyからyolo_detect_and_cut_person関数をインポート
from detection import sleeve_detection  # sleeve_detection.pyからyolo_detect_and_cut_sleeve関数をインポート
from file_system import create_or_find_output  # create_or_find_outputモジュールをインポート
from ir import Infrared_rays_send  # Infrared_rays_sendモジュールをインポート
from capture import time_capture  # time_captureモジュールをインポート
import shutil  # shutilモジュールをインポートして、ファイル操作を行う
from algorithm import algorithm_main  # algorithm.pyから必要な関数をインポート
from algorithm import file_manager  # ディレクトリ作成とデータ更新関数をインポート

log_dir = 'log'
current_dir = '.'

def capture_and_process_images():
    # outputディレクトリが存在しない場合は作成する
    create_or_find_output.create_or_find_output_dir(current_dir, log_dir)
    # logディレクトリが存在しない場合は作成する

    try:
        person_model = yolo_common.load_yolo_model('yolov8s')
        sleeve_model = yolo_common.load_yolo_model('best')
    except FileNotFoundError as e:
        print(e)
        return

    # 初期位置情報を取得
    location = algorithm_main.get_initial_location()
    # 室内温度のデフォルト値
    room_temperature = 25.0
    directory_paths = file_manager.create_directories()

    while True:
        print('画像撮影')
        image_data, capture_image_path = photographing.capture_image_data()
        print('画像撮影完了')
        
        if image_data is not None:
            print(f"Image data shape: {image_data.shape}")

            print('画像撮影に成功, なおかつimage_data is not None')
            timestamp = time_capture.get_current_timestamp()
            now_dir = create_or_find_output.create_or_find_output_dir(log_dir, timestamp)

            cv2.imwrite(capture_image_path, image_data)

            number_of_people, person_images = person_detection.yolo_detect_and_cut_person(image_data, now_dir, person_model)
            print(f"検出された人数: {number_of_people}")

            if number_of_people > 0:
                time.sleep(4)
                short_sleeve_count = 0
                long_sleeve_count = 0
                unknown_count = 0
                for person_image_path in person_images:
                    person_image = cv2.imread(person_image_path)
                    detected_sleeve = sleeve_detection.yolo_detect_and_cut_sleeve(person_image, now_dir, sleeve_model)
                    print(f"人物 {person_images.index(person_image_path) + 1} の識別結果: {detected_sleeve}")
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
                
                cooling_threshold, heating_threshold, status = algorithm_main.process_data(room_temperature, number_of_people, long_sleeve_count, short_sleeve_count, 0, location, directory_paths)
                
                # if cooling_threshold is not None and heating_threshold is not None:
                #     file_manager.update_data_file(room_temperature, cooling_threshold, heating_threshold, status, number_of_people, directory_paths)
                
                Infrared_rays_send.send_ir_command()
        
        # handle_switches からのデータをチェック
        if not shared_queue.empty():
            data_received = shared_queue.get()
            print(f"capture_and_process_imagesで受信したデータ: {data_received}")
            # 受信データが 0, 1, 2 の場合、"3"を書き込む
            if data_received in [0, 1, 2]:
                with open("output.txt", "a") as f:
                    f.write("3\n")
                # update_data_fileを呼び出す
                cooling_threshold, heating_threshold, status = algorithm_main.process_data(room_temperature, number_of_people, long_sleeve_count, short_sleeve_count, 0, location, directory_paths)
                file_manager.update_data_file(room_temperature, cooling_threshold, heating_threshold, data_received, number_of_people, directory_paths)

        # 20秒待機
        time.sleep(20)

if __name__ == "__main__":
    setup_gpio()
    threading.Thread(target=capture_and_process_images, daemon=True).start()
    threading.Thread(target=handle_switches, daemon=True).start()

    while True:
        time.sleep(0.1)  # メインスレッドをアイドル状態にする
