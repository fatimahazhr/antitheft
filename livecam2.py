import time
import requests
from ultralytics import YOLO
import cv2
import os

# --- CONFIG ---
MODEL_PATH = r"C:\Users\Acer\AI_OJD\runs\detect\train7\weights\best.pt"
OWNER_LABELS = ["fat"]       
CONF_THRESHOLD_FOR_OWNER = 0.75
MODEL_CONF_FILTER = 0.25
NOTIF_COOLDOWN_SECONDS = 5

# --- TELEGRAM CONFIG ---
BOT_TOKEN = "8145815062:AAFPHAnjIubioQPtRE5bdKadQKtm7L9R3tc"
CHAT_ID = "7362064891"

# --- FUNGSI KIRIM TEKS ---
def send_notification(payload: dict):
    message = (
        f"⚠️ Stranger Detected!\n"
        f"Predicted Label: {payload['label_predicted']}\n"
        f"Confidence: {payload['confidence']}\n"
        f"Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(payload['timestamp']))}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.get(url, params={"chat_id": CHAT_ID, "text": message}, timeout=5)
        print("[NOTIF TEXT SENT]", message)
    except Exception as e:
        print("[ERROR TELEGRAM MESSAGE]", e)

# --- FUNGSI KIRIM FOTO ---
def send_photo_to_telegram(image_path: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    try:
        with open(image_path, "rb") as img:
            requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": img}, timeout=5)
        print(f"[PHOTO SENT] {image_path}")
    except Exception as e:
        print("[ERROR SENDING PHOTO]", e)

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

            # Logika deteksi stranger
            if label in OWNER_LABELS:
                is_stranger = conf < CONF_THRESHOLD_FOR_OWNER
            else:
                is_stranger = True

            if is_stranger:
                box_color = (0, 0, 255)
                text_top = f"Stranger {conf:.2f}"
                now = time.time()

                if now - last_notif_time > NOTIF_COOLDOWN_SECONDS:
                    # --- Capture foto stranger ---
                    timestamp = int(now)
                    img_name = f"stranger_{timestamp}.jpg"
                    save_path = os.path.join(os.getcwd(), img_name)
                    cv2.imwrite(save_path, frame)
                    print(f"[CAPTURED] {save_path}")

                    # --- Kirim notifikasi teks ---
                    payload = {
                        "event": "stranger_detected",
                        "label_predicted": label,
                        "confidence": round(conf, 3),
                        "timestamp": now
                    }
                    send_notification(payload)

                    # --- Kirim foto ke telegram ---
                    send_photo_to_telegram(save_path)

                    last_notif_time = now

            else:
                box_color = (0, 255, 0)
                text_top = f" ({label}) {conf:.2f}"

            # Tampilkan kotak deteksi
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
