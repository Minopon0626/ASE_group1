"""
画像のパスを受け取りその画像内の物体を検出してトリミングした画像をoutputに入れるプログラム
"""
from ultralytics import YOLO
import file_path_finder
import create_or_find_output
import cv2
import os

def yolo_detect_and_cut(image_name):
    # YOLOv8モデルをロード
    model = YOLO("yolov8n.pt")  # ここで適切なモデルを指定します。例えば、yolov8n.pt（Nanoモデル）

    # 画像を読み込む
    image_path = file_path_finder.find_file_in_current_directory(image_name)  # ここで入力画像のパスを指定します
    if not image_path:
        print(f"{image_name} が見つかりませんでした")
        return

    image = cv2.imread(image_path)

    # 出力ディレクトリを設定
    output_dir = create_or_find_output.create_or_find_output_dir()
    os.makedirs(output_dir, exist_ok=True)

    # 画像に対して予測を行う
    results = model.predict(source=image_path)

    # クラス名のリスト（必要に応じて変更）
    class_names = model.names

    # 検出結果を処理
    object_count = {}
    for result in results:
        boxes = result.boxes  # バウンディングボックスを取得
        for box in boxes:
            # バウンディングボックスの座標を取得
            x1, y1, x2, y2 = box.xyxy[0].int().tolist()

            # 検出されたオブジェクトのクラスと信頼度を取得
            class_id = box.cls[0].item()
            class_name = class_names[class_id]
            confidence = box.conf[0].item()

            # オブジェクトの数をカウント
            if class_name not in object_count:
                object_count[class_name] = 0
            object_count[class_name] += 1

            # バウンディングボックス部分を切り抜き
            cropped_image = image[y1:y2, x1:x2]

            # 切り抜いた画像を保存
            output_filename = f"{class_name}_{object_count[class_name]}.jpeg"
            output_filepath = os.path.join(output_dir, output_filename)
            cv2.imwrite(output_filepath, cropped_image)

            # ログ出力
            print(f"検出されたオブジェクト: {class_name}, 信頼度: {confidence:.2f}, 保存ファイル: {output_filename}")

    # 全てのウィンドウを閉じる
    cv2.destroyAllWindows()
