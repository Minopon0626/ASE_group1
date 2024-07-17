from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("yolov8n.pt")

# Export the model to NCNN format
model.export(format="ncnn")  # creates '/yolov8n_ncnn_model'

# Load the exported NCNN model
ncnn_model = YOLO("./yolov8n_ncnn_model")

# Run inference
results = ncnn_model("photo_test_0.jpeg")