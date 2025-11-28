from ultralytics import YOLO

# Load model hasil training
model = YOLO(r"C:\Users\Acer\AI_OJD\runs\detect\train8\weights\best.pt")

# Jalankan deteksi real-time dari webcam
results = model.predict(
    source=0,     # 0 = default webcam
    show=True,    # tampilkan jendela video
    conf=0.85,     # confidence threshold
)
