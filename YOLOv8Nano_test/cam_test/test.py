# sudo apt update
# sudo apt install python3-opencv
import cv2

# カメラデバイスの初期化（通常はデバイスIDが0になります）
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("カメラデバイスを開けませんでした")
    exit()

# フレームをキャプチャ
ret, frame = cap.read()

if ret:
    # 画像を保存
    cv2.imwrite('captured_image.jpg', frame)
    print("画像を保存しました: captured_image.jpg")
else:
    print("フレームのキャプチャに失敗しました")

# カメラデバイスを解放
cap.release()
