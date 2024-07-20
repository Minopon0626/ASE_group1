import time
import os
import sys
import cv2
sys.path.append(os.path.join(os.path.dirname(__file__), 'detection'))
from capture import photographing
from detection import yolo_common
from detection import person_detection
from detection import sleeve_detection
from file_system import create_or_find_output
from ir import Infrared_rays_send
from capture import time_capture
import shutil

def main():
    log_dir = 'log'
    current_dir = '.'

    create_or_find_output.create_or_find_output_dir(current_dir, log_dir)

    try:
        person_model = yolo_common.load_yolo_model('yolov8s')
        sleeve_model = yolo_common.load_yolo_model('best')
    except FileNotFoundError as e:
        print(e)
        return

    while True:
        image_data, capture_image_path = photographing.capture_image()

        if image_data is not None:
            timestamp = time_capture.get_current_timestamp()
            now_dir = create_or_find_output.create_or_find_output_dir(log_dir, timestamp)

            # 保存するファイルパスを指定
            capture_image_path = os.path.join(now_dir, 'captured_image.jpg')
            cv2.imwrite(capture_image_path, image_data)

            # 人物検出を実行
            number_of_people, person_images = person_detection.yolo_detect_and_cut_person(capture_image_path, now_dir, person_model)
            print(f"検出された人数: {number_of_people}")

            if number_of_people > 0:
                time.sleep(4)
                short_sleeve_count = 0
                long_sleeve_count = 0
                unknown_count = 0
                for person_image_path in person_images:
                    person_image = cv2.imread(person_image_path)
                    detected_sleeve = sleeve_detection.yolo_detect_and_cut_sleeve(person_image_path, now_dir, sleeve_model)
                    print(f"人物 {person_images.index(person_image_path) + 1} の識別結果: {detected_sleeve}")
                    if detected_sleeve == "short_sleeve":
                        short_sleeve_count += 1
                        print(f"人物 {person_images.index(person_image_path) + 1}: 半袖")
                    elif detected_sleeve == "long_sleeve":
                        long_sleeve_count += 1
                        print(f"人物 {person_images.index(person_image_path) + 1}: 長袖")
                    else:
                        unknown_count += 1
                        print(f"人物 {person_images.index(person_image_path) + 1}: 不明")

                print(f"総計 - 半袖: {short_sleeve_count}, 長袖: {long_sleeve_count}, 不明: {unknown_count}")

                Infrared_rays_send.send_ir_command()

        time.sleep(20)

if __name__ == "__main__":
    main()
