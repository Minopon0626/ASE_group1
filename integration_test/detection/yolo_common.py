# yolo_common.py
from ultralytics import YOLO  # YOLOモデルを使用するためにultralyticsライブラリをインポート
import os

def load_yolo_model(model_name):
    model_dir = 'models'  # モデルが保存されているディレクトリ
    model_path = os.path.join(model_dir, f"{model_name}.pt")  # モデルファイルのパスを作成

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"モデル '{model_name}' が見つかりません。")

    # ultralytics YOLOを使用してモデルをロード
    model = YOLO(model_path)
    
    return model

def write_log(log_file_path, class_name, confidence, output_filename):
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"検出されたオブジェクト: {class_name}, 信頼度: {confidence:.2f}, 保存ファイル: {output_filename}\n")
