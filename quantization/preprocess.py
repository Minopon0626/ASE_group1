#入力画像の前処理と推論の実行
import cv2

def preprocess_image(image_path, target_size=(640, 640)):
    # 画像の読み込み
    image = cv2.imread(image_path)
    
    # 画像のリサイズ
    resized_image = cv2.resize(image, target_size)
    
    # 画像の標準化
    input_data = resized_image.astype(np.float32) / 255.0
    
    # バッチ次元の追加
    input_data = np.expand_dims(input_data, axis=0)
    
    return input_data

# 入力画像の前処理
input_data = preprocess_image('YOLOv8Nano_test/photo_test_0.jpeg')

# 入力データの設定
interpreter.set_tensor(input_details[0]['index'], input_data)

# 推論の実行
interpreter.invoke()

# 結果の取得
output_data = interpreter.get_tensor(output_details[0]['index'])
print(output_data)