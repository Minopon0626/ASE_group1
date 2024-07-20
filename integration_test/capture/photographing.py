"""
関数が読みだされた際に一回撮影するpythonプログラム
撮影して保存したファイルパスを返す
"""
# photographing.py
import os
import cv2

def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("カメラデバイスを開けませんでした")
        return None, None

    ret, frame = cap.read()

    if ret:
        file_path = os.path.abspath('captured_image.jpg')
        output_dir = os.path.dirname(file_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            cv2.imwrite(file_path, frame)
            print(f"画像を保存しました: {file_path}")
            return frame, file_path
        except Exception as e:
            print(f"画像の保存中にエラーが発生しました: {e}")
            return None, None
    else:
        print("フレームのキャプチャに失敗しました")
        return None, None

    cap.release()
