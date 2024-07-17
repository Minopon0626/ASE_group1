from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model("photo_test_0.jpeg") 