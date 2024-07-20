import cv2
import os
from file_system import file_path_finder  # ファイル検索のためのモジュールをインポート
from yolo_common import load_yolo_model, write_log

def yolo_detect_and_cut_sleeve(image_data, output_dir, model):
    # 出力ディレクトリを設定
    os.makedirs(output_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成

    log_file_path = os.path.join(output_dir, "log.txt")  # logファイルの指定

    # 画像に対して予測を行う
    results = model.predict(source=image_data)  # YOLOモデルを使用して画像の物体検出を行う

    # クラス名のリスト（必要に応じて変更）
    class_names = model.names  # モデルが認識するクラス名のリストを取得

    detected_sleeve = "unknown"  # デフォルトは不明

    for result in results:
        boxes = result.boxes  # バウンディングボックスを取得
        for box in boxes:
            # バウンディングボックスの座標を取得
            x1, y1, x2, y2 = box.xyxy[0].int().tolist()  # 座標を整数リストに変換

            # 検出されたオブジェクトのクラスと信頼度を取得
            class_id = box.cls[0].item()  # クラスIDを取得
            class_name = class_names[class_id]  # クラス名を取得
            confidence = box.conf[0].item()  # 信頼度を取得

            # クラス名が "sleeve" の場合、半袖と長袖を識別
            if class_name == "sleeve":
                detected_sleeve = "hansode" if confidence > 0.5 else "nagasode"
                # 半袖か長袖かを信頼度に基づいて判断（ここでは例として信頼度 > 0.5 の場合を半袖とする）

                # ログ出力
                output_filename = "sleeve.jpeg"  # 保存するファイル名を生成
                output_filepath = os.path.join(output_dir, output_filename)  # 保存先のパスを生成
                cv2.imwrite(output_filepath, image_data)  # 画像を保存
                write_log(log_file_path, class_name, confidence, output_filename)
                print(f"検出された袖: {detected_sleeve}, 信頼度: {confidence:.2f}, 保存ファイル: {output_filename}")

    # 全てのウィンドウを閉じる
    cv2.destroyAllWindows()  # OpenCVのウィンドウをすべて閉じる

    return detected_sleeve  # 識別された袖の種類を返す
