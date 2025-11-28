from ultralytics import YOLO
import cv2
import csv
import time

# Memuat model YOLO
model = YOLO("C:/Users/Acer/AI_training/runs/detect/train/weights/best.pt")  # Ganti dengan path ke model yang sesuai

with open('detect.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Timestamp", "Detected Item", "Confidence"])


    # Membuka video (0 untuk webcam)
    video_path = 0
    cap = cv2.VideoCapture(video_path)
    
   
    
    if not cap.isOpened():
        print("can't open camera")
        exit()
    # Loop melalui frame video
    while cap.isOpened():
        # Membaca frame dari video
        success, frame = cap.read()
        if not success:
            break
        if success:
            # Menjalankan inferensi YOLO pada frame
            results = model.predict(frame, imgsz = 320, conf = 0.5)
    
            # Memeriksa apakah ada deteksi objek
            result = results[0]
            boxes = result.boxes.xyxy.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
                # detections = result.boxes.xyxy  # Mendapatkan koordinat bounding box
                # classes = result.boxes.cls  # Mendapatkan kelas objek
    
            for box,cls,conf in zip(boxes, classes, confidences):
                x1,y1,x2,y2 = map (int, box)
                cv2.rectangle(frame,(x1,y1), (x2,y2), (0,255,0),4)
                label = f"{model.names[int(cls)]} {conf:.2f}"
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 4)
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                writer.writerow([timestamp, model.names[int(cls)], conf])
            # Menampilkan frame yang telah dianotasi
            cv2.imshow("YOLO Inference", frame)
    
            # Menghentikan proses jika 'q' ditekan
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Menghentikan loop jika akhir video tercapai
            break

# Melepaskan objek video dan menutup semua jendela
cap.release()
cv2.destroyAllWindows()