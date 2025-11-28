from ultralytics import YOLO

# load model (bisa ganti dengan 'yolov8n.pt', 'yolov8s.pt', dst)
model = YOLO("yolov8n.pt")

# training
model.train(
    data=r"C:\Users\Acer\AI_OJD\data.yaml",
    epochs=50,
    imgsz=640,
    batch=16,
)
