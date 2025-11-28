import time
import requests
from ultralytics import YOLO
import cv2

# --- CONFIG ---
MODEL_PATH = r"C:\Users\Acer\AI_OJD\runs\detect\train8\weights\best.pt"
OWNER_LABELS = ["fat", "vincent"]       # label wajah pemilik
CONF_THRESHOLD_FOR_OWNER = 0.75          # kalau di bawah ini dianggap stranger
MODEL_CONF_FILTER = 0.25
NOTIF_COOLDOWN_SECONDS = 5

# --- TELEGRAM CONFIG ---
BOT_TOKEN = "8145815062:AAFPHAnjIubioQPtRE5bdKadQKtm7L9R3tc"
CHAT_ID = "7362064891"

# --- FUNGSI KIRIM NOTIF TELEGRAM ---
# def send_notification(payload: dict):
#     message = (
#         f"⚠️ Stranger Detected!\n"
#         f"Predicted Label: {payload['label_predicted']}\n"
#         f"Confidence: {payload['confidence']}\n"
#         f"Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(payload['timestamp']))}"
#     )
#     url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
#     try:
#         requests.get(url, params={"chat_id": CHAT_ID, "text": message}, timeout=5)
#         print("[NOTIFICATION SENT TO TELEGRAM]", message)
#     except Exception as e:
#         print("[ERROR SENDING TELEGRAM MESSAGE]", e)

# --- LOAD MODEL ---
model = YOLO(MODEL_PATH)

# --- OPEN WEBCAM ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Cannot open webcam (index 0).")

last_notif_time = 0.0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=MODEL_CONF_FILTER, verbose=False)
        if len(results) == 0:
            cv2.imshow("Anti-Theft", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        res = results[0]
        if not hasattr(res, "boxes") or len(res.boxes) == 0:
            cv2.imshow("Anti-Theft", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        for box in res.boxes:
            conf = float(box.conf.cpu().numpy()) if hasattr(box.conf, "cpu") else float(box.conf)
            cls = int(box.cls.cpu().numpy()) if hasattr(box.cls, "cpu") else int(box.cls)
            label = model.names[cls] if cls in model.names else str(cls)
            xyxy = box.xyxy[0]
            x1, y1, x2, y2 = map(int, xyxy)

            # ✅ logika deteksi
            if label in OWNER_LABELS:
                if conf < CONF_THRESHOLD_FOR_OWNER:
                    is_stranger = True
                else:
                    is_stranger = False
            else:
                is_stranger = True  # label lain otomatis stranger

            # tampilkan hasil
            if is_stranger:
                box_color = (0, 0, 255)
                text_top = f"Stranger {conf:.2f}"
                now = time.time()
                if now - last_notif_time > NOTIF_COOLDOWN_SECONDS:
                    payload = {
                        "event": "stranger_detected",
                        "label_predicted": label,
                        "confidence": round(conf, 3),
                        "timestamp": now
                    }
                    # send_notification(payload)
                    # last_notif_time = now
            else:
                box_color = (0, 255, 0)
                text_top = f" ({label}) {conf:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            cv2.putText(frame, text_top, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)

            if is_stranger:
                cv2.putText(frame, "⚠️ STRANGER", (x1, y2 + 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Anti-Theft", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
