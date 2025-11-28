import cv2
import mediapipe as mp

# Load face detector dari OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils  # Untuk menggambar hasil deteksi

# Fungsi untuk menghitung jumlah jari yang terangkat
def count_fingers(hand_landmarks):
    # Tentukan ID untuk setiap ujung jari
    finger_tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Ibu jari: periksa apakah ujung ibu jari lebih jauh dari landmark ibu jari lainnya
    if hand_landmarks.landmark[finger_tips_ids[0]].x < hand_landmarks.landmark[finger_tips_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Empat jari lainnya
    for tip_id in finger_tips_ids[1:]:
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    # Mengembalikan jumlah jari yang terangkat
    return fingers.count(1)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Deteksi Wajah
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    num_faces = len(faces)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Deteksi Tangan
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Konversi ke RGB untuk MediaPipe
    results = hands.process(rgb_frame)

    # Gambar deteksi tangan dan hitung jumlah jari yang terangkat
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            finger_count = count_fingers(hand_landmarks)  # Hitung jari yang terangkat
            
            # Tampilkan jumlah jari yang terangkat pada layar
            cv2.putText(frame, f"Fingers Up = {finger_count}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Tampilkan jumlah wajah yang terdeteksi
    cv2.putText(frame, f"Face Detected = {num_faces}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Tampilkan hasil pada jendela
    cv2.imshow("Real Time Face and Hand Detection", frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Lepaskan resource
cap.release()
cv2.destroyAllWindows()
