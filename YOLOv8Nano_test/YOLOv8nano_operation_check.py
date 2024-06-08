# pip install ultralytics opencv-python　をしたらこのコードは実行可能なはず
"""
YOLOv8nanoを利用した画像内検知を行う
検知したオブジェクトとその信頼性, 座標を標準出力に返す
"""

from ultralytics import YOLO

# YOLOv8モデルをロード
model = YOLO("yolov8n.pt")  # ここで適切なモデルを指定します。例えば、yolov8n.pt（Nanoモデル）

# 画像を読み込む
image_path = "D:\\vscodeWorkSpace\\ASE_group1\\photo_test_0.jpeg"  # ここで入力画像のパスを指定します
results = model.predict(source=image_path)

# 検出結果を処理
for result in results:
    boxes = result.boxes  # バウンディングボックスを取得
    for box in boxes:
        # バウンディングボックスの座標を取得
        x1, y1, x2, y2 = box.xyxy[0].int().tolist()

        # 検出されたオブジェクトのクラスと信頼度を取得
        class_id = box.cls[0].item()
        confidence = box.conf[0].item()

        # 出力を日本語に翻訳して表示
        print(f"検出されたオブジェクトのクラス: {class_id}, 信頼度: {confidence}, バウンディングボックス: ({x1}, {y1}, {x2}, {y2})")
