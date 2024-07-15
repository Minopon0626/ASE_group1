import os  # osモジュールをインポートして、OSとの対話を行う
from capture_and_detection import capture_and_process_video  # capture_and_detection.pyから関数をインポート
from detection.ImageDetection import load_yolo_model  # ImageDetection.pyからload_yolo_model関数をインポート
from file_system import create_or_find_output  # create_or_find_outputモジュールをインポート

def main():
    log_dir = 'log'  # logディレクトリ名
    current_dir = '.'
    create_or_find_output.create_or_find_output_dir(current_dir, log_dir)

    yolo_model = load_yolo_model()
    
    # 動画をリアルタイム処理
    capture_and_process_video(yolo_model, output_dir=log_dir)

if __name__ == "__main__":
    main()
