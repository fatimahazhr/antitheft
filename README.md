# 🚗 Anti-Theft Driver Recognition System

*Real-time unknown driver detection using YOLO and Telegram alert*

---

## 📌 Background

Kasus pencurian kendaraan masih sering terjadi, terutama pada kendaraan yang belum dilengkapi sistem keamanan berbasis identitas. Sistem anti-theft tradisional seperti alarm atau immobilizer tidak mampu mengenali siapa yang sebenarnya mengemudikan kendaraan.

Project ini dikembangkan untuk membuat **Anti-Theft System berbasis Computer Vision**, yang mampu:

* Mendeteksi wajah pengemudi secara real-time
* Mengidentifikasi apakah pengemudi adalah **owner** atau **stranger**
* Mengirimkan **notifikasi Telegram + foto** ketika orang asing masuk ke kendaraan
* Berjalan menggunakan perangkat minimal (laptop + webcam)

Alasan pemilihan topik:

* Sistem keamanan berbasis wajah sulit dipalsukan
* Dapat diintegrasikan dengan teknologi IoV (Internet of Vehicle)
* Implementasi lightweight dan scalable untuk otomotif modern

---

## 📂 Dataset

Dataset merupakan dataset wajah custom untuk single-class detection.

### **1. Data Owner**

* Class: `"fat"`
* 95 gambar wajah
* Variasi pose & pencahayaan
* Format: `.jpg`

### **2. Data Non-owner (negatif)**

(Tidak digunakan untuk training → model hanya belajar mengenali owner)
Non-owner dikenali melalui *logic* di aplikasi (fail-safe).

### **3. Labeling**

* Tool: **LabelImg**
* Format annotation: YOLO (`.txt` per image)

---

## 🧠 Model

Model yang digunakan:

### **✨ YOLOv8 Custom Training**

* Base: `YOLOv8n` (lightweight)
* Task: single-class detection
* Framework: Ultralytics YOLO
* Output model:

  ```
  runs/detect/train7/weights/best.pt
  ```

### **Hyperparameters**

* `MODEL_CONF_FILTER = 0.25` → confidence minimum untuk menampilkan deteksi
* `CONF_THRESHOLD_FOR_OWNER = 0.75`

  * Jika wajah terdeteksi sebagai owner tapi confidence < 0.75 → dianggap stranger
  * Fail-safe untuk menghindari false-positive

---

## 📈 Model Performance (Metrics)

<img width="2400" height="1200" alt="results" src="https://github.com/user-attachments/assets/aa54c36a-08ec-4d52-bff0-c1fef8d69d99" />

**Ringkasan hasil training:**

* mAP50: **0.992**
* mAP50-95: **0.848**
* Precision: **0.99**
* Recall: **0.98**

Contoh prediksi validation batch:

![val\_batch1\_pred](https://github.com/user-attachments/assets/bfd6d58c-ea42-4ae2-866e-a55e4ed5de62)

Confusion matrix:

<img width="3000" height="2250" alt="confusion_matrix" src="https://github.com/user-attachments/assets/d9af6029-2cd2-4c35-8f45-b56e0b0b59f0" />

---

## 🧩 System Architecture / Flow

1. Webcam mengambil gambar secara real-time
2. Model YOLO mendeteksi wajah
3. Sistem mengklasifikasikan:

   * **Owner → label = fat, conf ≥ 0.75**
   * **Stranger → label ≠ fat atau conf < 0.75**
4. Jika stranger:

   * Capture frame
   * Kirim notifikasi Telegram
   * Kirim foto stranger
5. Tampilkan bounding box:

   * 🟢 Hijau = owner
   * 🔴 Merah = stranger

---

## 🧪 How to Run

### **1. Clone Repository**

```bash
git clone https://github.com/fatimahazhr/antitheft.git
cd antitheft
```

### **2. Install Dependencies**

```bash
pip install ultralytics opencv-python requests
```

### **3. Download / Copy Model**

Letakkan file:

```
best.pt  → runs/detect/train7/weights/best.pt
```

### **4. Jalankan Program**

```bash
python livecam2.py
```

---

## 📁 Project Structure

```
📦 Anti-Theft
├── 📂 runs/
│   └── detect/train7/weights/best.pt
├── 📂 dataset/
│   ├── images/
│   └── labels/
├── livecam2.py
├── README.md
└── requirements.txt
```

---

## 📬 Telegram Integration

Sistem mengirimkan alert melalui Telegram API:

* Notifikasi teks (label + confidence + waktu)
* Foto stranger
* Cooldown notifikasi: **5 detik**

> **Security Note:**
> Jangan pernah commit bot token ke repository publik.
> Gunakan environment variable:
>
> ```
> BOT_TOKEN = os.getenv("BOT_TOKEN")
> ```

---

## 📝 Conclusion

Sistem Anti-Theft Driver Recognition ini berhasil membuktikan bahwa:

* Pengenalan pengemudi menggunakan YOLO dapat bekerja secara real-time
* Dengan hanya satu class (owner), sistem tetap dapat mendeteksi stranger melalui fail-safe logic
* Integrasi Telegram membuat respon terhadap risiko pencurian menjadi lebih cepat
* Sistem ringan dan dapat digunakan sebagai dasar teknologi keamanan kendaraan modern

---

## 🚀 Future Work

* Menambah multi-owner recognition
* Integrasi dengan IoV (engine lock melalui CAN Bus)
* Menambah dataset non-owner untuk meningkatkan robustness
* Penanganan low light dan occlusion
* Mobile app untuk notifikasi terintegrasi

