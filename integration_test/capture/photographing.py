"""
関数が読みだされた際に一回撮影するpythonプログラム
撮影して保存したファイルパスを返す
"""
import os  # ファイルパスの操作に必要なライブラリをインポート
import cv2  # OpenCVライブラリをインポートして、画像処理やカメラ操作を行う

def capture_image():
    # カメラデバイスの初期化（通常はデバイスIDが0になります）
    cap = cv2.VideoCapture(0)  # デバイスID0でカメラを初期化

    if not cap.isOpened():
        # カメラデバイスが開けない場合の処理
        print("カメラデバイスを開けませんでした")
        return None  # Noneを返して終了

    # フレームをキャプチャ
    ret, frame = cap.read()  # カメラからフレームをキャプチャ

    if ret:
        # フレームのキャプチャに成功した場合
        # 画像を保存
        file_path = os.path.abspath('captured_image.jpg')  # 絶対パスを取得
        cv2.imwrite(file_path, frame)  # フレームを画像ファイルとして保存
        print(f"画像を保存しました: {file_path}")
        return file_path  # 保存した画像のファイルパスを返す
    else:
        # フレームのキャプチャに失敗した場合
        print("フレームのキャプチャに失敗しました")
        return None  # Noneを返して終了

    # カメラデバイスを解放
    cap.release()  # カメラデバイスを解放してリソースをクリア
