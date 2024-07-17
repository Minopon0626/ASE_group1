from ultralytics import YOLO

model = YOLO('../runs/detect/train/weights/last.pt')

# Predict the model
model.predict('test2.jpg', save=True, conf=0.1)
