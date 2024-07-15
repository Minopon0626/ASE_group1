# 必要なライブラリをインストール
# pip install ultralytics

# モデルのトレーニング
from ultralytics import YOLO

# モデルをロード
model = YOLO('yolov8s.pt')  # 他のモデルサイズも使用可能

# データセットのパスを設定
data_yaml = 'data.yaml'

# モデルをトレーニング
model.train(data=data_yaml, epochs=100, imgsz=640)

# モデルの検証
model.val(data=data_yaml)

# 推論の実行
results = model('D:\vscodefolder\ASE_group1\training\hansode_91.jpg')

# 結果を表示
results.show()

# トレーニング済みモデルの保存
model.save('hansode_yolov8_model.pt')
