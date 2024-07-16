#モデルの量子化

import tensorflow as tf

# 元のKerasモデルの読み込み
model = tf.keras.models.load_model('YOLOv8Nano_test/yolov8m.pt')

# TFLiteConverterを使ってモデルを量子化
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# 量子化モデルの変換
quantized_model = converter.convert()

# 量子化モデルの保存
with open('quantized_model.tflite', 'wb') as f:
    f.write(quantized_model)