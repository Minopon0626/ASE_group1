#
"""
関数が読みだされた際に一回撮影するpythonプログラム
"""
import cv2

def capture_image():
    # カメラデバイスの初期化（通常はデバイスIDが0になります）
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("カメラデバイスを開けませんでした")
        return None

    # フレームをキャプチャ
    ret, frame = cap.read()

    if ret:
        # 画像を保存
        cv2.imwrite('captured_image.jpg', frame)
        print("画像を保存しました: captured_image.jpg")
        return 'captured_image.jpg'
    else:
        print("フレームのキャプチャに失敗しました")
        return None

    # カメラデバイスを解放
    cap.release()
