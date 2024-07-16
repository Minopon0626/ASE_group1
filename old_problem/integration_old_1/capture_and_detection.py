import os  # ファイルパスの操作に必要なライブラリをインポート
import cv2  # OpenCVライブラリをインポートして、画像処理やカメラ操作を行う
import time  # timeモジュールをインポートして、時間関連の操作を行う
from detection.ImageDetection import load_yolo_model  # ImageDetection.pyから関数をインポート
from ir import Infrared_rays_send  # Infrared_rays_sendモジュールをインポート
from file_system import create_or_find_output  # create_or_find_outputモジュールをインポート
from capture import time_capture  # time_captureモジュールをインポート

def capture_and_process_video(yolo_model, output_dir='output'):
    # カメラデバイスの初期化（通常はデバイスIDが0になります）
    cap = cv2.VideoCapture(0)  # デバイスID0でカメラを初期化

    if not cap.isOpened():
        # カメラデバイスが開けない場合の処理
        print("カメラデバイスを開けませんでした")
        return  # 終了

    while True:
        ret, frame = cap.read()
        if ret:
            # YOLOでフレームを処理
            results = yolo_model.predict(source=frame)
            person_count = 0
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].int().tolist()
                    class_id = box.cls[0].item()
                    class_name = yolo_model.names[class_id]
                    confidence = box.conf[0].item()
                    if class_name == "person":
                        person_count += 1
                        # 検出された人をハイライト
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, f"{class_name} {confidence:.2f}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # 現在時刻を取得
            timestamp = time_capture.get_current_timestamp()
            log_file_path = os.path.join(output_dir, "log.txt")
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"{timestamp}, 検出された人数: {person_count}\n")

            # 検出結果を表示
            cv2.imshow('Real-time YOLO Detection', frame)

            # 検出された人数が1人以上ならIRコマンドを送信
            if person_count > 0:
                Infrared_rays_send.send_ir_command()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("フレームのキャプチャに失敗しました")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    yolo_model = load_yolo_model()
    capture_and_process_video(yolo_model)
