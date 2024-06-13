"""
関数が読みだされた際に一回撮影するpythonプログラム
"""
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
        cv2.imwrite('captured_image.jpg', frame)  # フレームを画像ファイルとして保存
        print("画像を保存しました: captured_image.jpg")
        return 'captured_image.jpg'  # 保存した画像のファイル名を返す
    else:
        # フレームのキャプチャに失敗した場合
        print("フレームのキャプチャに失敗しました")
        return None  # Noneを返して終了

    # カメラデバイスを解放
    cap.release()  # カメラデバイスを解放してリソースをクリア
