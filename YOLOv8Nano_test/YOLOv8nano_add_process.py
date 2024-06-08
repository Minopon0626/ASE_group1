"""
YOLOv8nanoを利用して検知した後に検知する
検知したオブジェクトを四角で囲う
検知したオブジェクトの詳細情報を追記する
"""
from ultralytics import YOLO
import cv2
import file_path_finder
import create_or_find_output

# YOLOv8モデルをロード
model = YOLO("yolov8n.pt")  # ここで適切なモデルを指定します。例えば、yolov8n.pt（Nanoモデル）

# 画像を読み込む
image_name = "photo_test_0.jpeg"

image_path = file_path_finder.find_file_in_current_directory(image_name)  # ここで入力画像のパスを指定します
image = cv2.imread(image_path)

# 画像に対して予測を行う
results = model.predict(source=image_path)

# クラス名のリスト（必要に応じて変更）
class_names = model.names

# 検出結果を処理
for result in results:
    boxes = result.boxes  # バウンディングボックスを取得
    for box in boxes:
        # バウンディングボックスの座標を取得
        x1, y1, x2, y2 = box.xyxy[0].int().tolist()

        # 検出されたオブジェクトのクラスと信頼度を取得
        class_id = box.cls[0].item()
        confidence = box.conf[0].item()
        
        # バウンディングボックスを描画
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # クラス名と信頼度を描画
        label = f"{class_names[class_id]}: {confidence:.2f}"
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# 結果画像を保存または表示
output_dir = create_or_find_output.create_or_find_output_dir()
cv2.imwrite(output_dir, image)
cv2.imshow("Detected Objects", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
