import cv2
from ultralytics import YOLO

# Load model YOLOv8
model = YOLO("yolov8n.pt")

# Buka video (0 untuk kamera bawaan)
video_path = 0
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Jalankan YOLO untuk deteksi
    results = model(frame)

    # Ambil semua kotak batas deteksi
    boxes = results[0].boxes

    # Variabel untuk menandai apakah panggilan telepon terdeteksi
    is_on_call = False

    for box in boxes:
        class_id = int(box.cls[0])  # Ambil ID kelas deteksi
        confidence = box.conf[0]  # Ambil confidence dari deteksi

        # Cari ID kelas "hand" atau "phone" dalam dictionary model.names
        if model.names.get(class_id) in ["hand", "cell phone"]:
            is_on_call = True  # Tandai jika ditemukan objek tangan atau ponsel
            break

    # Jika mendeteksi tangan atau ponsel, tampilkan notifikasi
    annotated_frame = results[0].plot()
    if is_on_call:
        cv2.putText(annotated_frame, "OJO HP AN", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Tampilkan hasil
    cv2.imshow("YOLO inference", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Lepaskan resource
cap.release()
cv2.destroyAllWindows()
