#pytorchの量子化

import torch
from ultralytics import YOLO

# モデルの読み込み
model = YOLO("yolov8n.pt")
model.eval()  # 評価モードに設定

# モデルを量子化対応に変換
model.qconfig = torch.quantization.get_default_qconfig('photo_test_0.jpeg')
torch.quantization.prepare(model, inplace=True)

# キャリブレーション用のデータを用意
def calibrate(model, data_loader):
    model.eval()
    with torch.no_grad():
        for inputs, _ in data_loader:
            model(inputs)

# キャリブレーション用のデータローダーを準備（例）
# 実際には適切なデータセットを使用
data_loader = torch.utils.data.DataLoader(calibration_dataset, batch_size=32)

# キャリブレーション実行
calibrate(model, data_loader)

#量子化の実行: モデルを量子化します。
torch.quantization.convert(model, inplace=True)


# テスト用データローダーを準備（例）
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=32)

# 量子化されたモデルの性能を評価
def evaluate(model, data_loader):
    model.eval()
    accuracy = 0
    with torch.no_grad():
        for inputs, labels in data_loader:
            outputs = model(inputs)
            # 精度計算の処理（例）
            accuracy += (outputs.argmax(dim=1) == labels).float().mean().item()
    return accuracy / len(data_loader)

test_accuracy = evaluate(model, test_loader)
print(f"Test Accuracy after quantization: {test_accuracy:.4f}")