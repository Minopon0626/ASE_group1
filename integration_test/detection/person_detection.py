import cv2
import os
from yolo_common import write_log

def yolo_detect_and_cut_person(image_data, output_dir, model):
    # 出力ディレクトリを設定
    os.makedirs(output_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成

    log_file_path = os.path.join(output_dir, "log.txt")  # logファイルの指定

    # 画像に対して予測を行う
    results = model.predict(source=image_data)  # YOLOモデルを使用して画像の物体検出を行う

    # クラス名のリスト（必要に応じて変更）
    class_names = model.names  # モデルが認識するクラス名のリストを取得

    # 検出結果を処理
    object_count = {}  # 各オブジェクトの数をカウントするための辞書
    person_count = 0  # 人が検出された数をカウントする変数
    person_images = []  # 切り抜き画像のパスを保存するリスト

    for result in results:
        boxes = result.boxes  # バウンディングボックスを取得
        for box in boxes:
            # バウンディングボックスの座標を取得
            x1, y1, x2, y2 = box.xyxy[0].int().tolist()  # 座標を整数リストに変換

            # 検出されたオブジェクトのクラスと信頼度を取得
            class_id = box.cls[0].item()  # クラスIDを取得
            class_name = class_names[class_id]  # クラス名を取得
            confidence = box.conf[0].item()  # 信頼度を取得

            # オブジェクトの数をカウント
            if class_name not in object_count:
                object_count[class_name] = 0  # 初めてのクラス名の場合、辞書に追加
            object_count[class_name] += 1  # カウントを増やす

            # 人が検出された場合のフラグを更新
            if class_name == "person":
                person_count += 1  # 人のカウントを増やす

                # バウンディングボックス部分を切り抜き
                cropped_image = image_data[y1:y2, x1:x2]  # バウンディングボックスの部分を切り抜く

                # 切り抜いた画像を保存
                output_filename = f"{class_name}_{object_count[class_name]}.jpeg"  # 保存するファイル名を生成
                output_filepath = os.path.join(output_dir, output_filename)  # 保存先のパスを生成
                cv2.imwrite(output_filepath, cropped_image)  # 画像を保存

                # 人の切り抜き画像パスをリストに追加
                person_images.append(output_filepath)

            # ログ出力
            write_log(log_file_path, class_name, confidence, output_filename)
            print(f"検出されたオブジェクト: {class_name}, 信頼度: {confidence:.2f}, 保存ファイル: {output_filename}")

    # 全てのウィンドウを閉じる
    cv2.destroyAllWindows()  # OpenCVのウィンドウをすべて閉じる

    return person_count, person_images  # 検出された人の数と切り抜き画像のパスリストを返す
