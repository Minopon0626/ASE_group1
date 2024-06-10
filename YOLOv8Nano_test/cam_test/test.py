# sudo apt update
# sudo apt install python3-opencv
# sudo apt install v4l-utils
import cv2
import subprocess

def get_camera_device_number():
    result = subprocess.run(['v4l2-ctl', '--list-devices'], capture_output=True, text=True)
    devices_info = result.stdout

    devices = []
    lines = devices_info.split('\n')
    for i, line in enumerate(lines):
        if '/dev/video' in line:
            devices.append(line.strip())

    if len(devices) > 0:
        # 最初のカメラデバイスを使用（必要に応じて変更可能）
        return devices[0]
    else:
        return None

camera_device = get_camera_device_number()

if camera_device is None:
    print("カメラデバイスが見つかりませんでした")
    exit()

# デバイス番号を取得
device_number = int(camera_device.replace('/dev/video', ''))

# カメラデバイスの初期化
cap = cv2.VideoCapture(device_number)

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
