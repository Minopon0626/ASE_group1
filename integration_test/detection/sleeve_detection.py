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

    # 信頼度を格納する辞書
    max_confidence = {"hansode": 0, "nagasode": 0}

    # 検出結果を処理
    for result in results:
        boxes = result.boxes  # バウンディングボックスを取得
        for box in boxes:
            # バウンディングボックスの座標を取得
            x1, y1, x2, y2 = box.xyxy[0].int().tolist()  # 座標を整数リストに変換

            # 検出されたオブジェクトのクラスと信頼度を取得
            class_id = box.cls[0].item()  # クラスIDを取得
            class_name = class_names[class_id]  # クラス名を取得
            confidence = box.conf[0].item()  # 信頼度を取得

            # クラス名が "hansode" または "nagasode" の場合
            if class_name in max_confidence:
                if confidence > max_confidence[class_name]:
                    max_confidence[class_name] = confidence
                    detected_sleeve = class_name
                # 信頼度が最も高いクラスを更新

    # 検出結果に基づくデフォルトの袖の種類
    if max_confidence["hansode"] > max_confidence["nagasode"]:
        detected_sleeve = "hansode"
    elif max_confidence["nagasode"] > max_confidence["hansode"]:
        detected_sleeve = "nagasode"
    else:
        detected_sleeve = "unknown"

    # 最も信頼度が高い袖の種類の画像を保存
    if detected_sleeve != "unknown":
        output_filename = f"{detected_sleeve}.jpeg"  # 保存するファイル名を生成
        output_filepath = os.path.join(output_dir, output_filename)  # 保存先のパスを生成
        cv2.imwrite(output_filepath, image_data)  # 画像を保存
        write_log(log_file_path, detected_sleeve, max_confidence[detected_sleeve], output_filename)
        print(f"検出された袖: {detected_sleeve}, 信頼度: {max_confidence[detected_sleeve]:.2f}, 保存ファイル: {output_filename}")

    # 全てのウィンドウを閉じる
    cv2.destroyAllWindows()  # OpenCVのウィンドウをすべて閉じる

    return detected_sleeve  # 識別された袖の種類を返す
