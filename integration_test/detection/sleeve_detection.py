# sleeve_detection.py
import cv2
import os
from file_system import file_path_finder  # ファイル検索のためのモジュールをインポート
from yolo_common import load_yolo_model, write_log

def yolo_detect_and_cut_sleeve(image_name, output_dir, model):
    # 画像を読み込む
    image_path = file_path_finder.find_file_in_current_directory(image_name)  # ここで入力画像のパスを指定します
    if not image_path:
        # 画像が見つからない場合の処理
        print(f"{image_name} が見つかりませんでした")
        return 0  # 検出されなかったことを示すために0を返す

    image = cv2.imread(image_path)  # 画像ファイルを読み込む

    # 出力ディレクトリを設定
    os.makedirs(output_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成

    log_file_path = os.path.join(output_dir, "log.txt")  # logファイルの指定

    # 画像に対して予測を行う
    results = model.predict(source=image_path)  # YOLOモデルを使用して画像の物体検出を行う

    # クラス名のリスト（必要に応じて変更）
    class_names = model.names  # モデルが認識するクラス名のリストを取得

    # 検出結果を処理
    object_count = {}  # 各オブジェクトの数をカウントするための辞書

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

            # バウンディングボックス部分を切り抜き
            cropped_image = image[y1:y2, x1:x2]  # バウンディングボックスの部分を切り抜く

            # 切り抜いた画像を保存
            output_filename = f"{class_name}_{object_count[class_name]}.jpeg"  # 保存するファイル名を生成
            output_filepath = os.path.join(output_dir, output_filename)  # 保存先のパスを生成
            cv2.imwrite(output_filepath, cropped_image)  # 画像を保存

            # ログ出力
            write_log(log_file_path, class_name, confidence, output_filename)
            print(f"検出されたオブジェクト: {class_name}, 信頼度: {confidence:.2f}, 保存ファイル: {output_filename}")
            # 検出結果をコンソールに出力

    # 全てのウィンドウを閉じる
    cv2.destroyAllWindows()  # OpenCVのウィンドウをすべて閉じる

    return object_count  # 検出されたオブジェクトの数を返す
