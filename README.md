# 🚗 Anti-Theft Driver Recognition System

*Real-time unknown driver detection using YOLO and Telegram alert*

---

## 📌 **Background**

Kasus pencurian kendaraan semakin meningkat, terutama pada kendaraan tanpa sistem keamanan tambahan. Salah satu kelemahan sistem keamanan konvensional seperti alarm adalah tidak adanya identifikasi pengemudi secara langsung.

Project ini dikembangkan untuk membuat **Anti-Theft System berbasis Computer Vision**, yang mampu:

* Mendeteksi wajah pengemudi secara real-time
* Mengidentifikasi apakah pengemudi adalah **owner** atau **stranger**
* Mengirimkan **notifikasi Telegram + foto pengemudi** jika ada orang tak dikenal mencoba mengemudikan kendaraan
* Menggunakan perangkat minimal: laptop + webcam

Pemilihan topik ini dilakukan karena:

* Sistem keamanan berbasis identitas wajah jauh lebih sulit dipalsukan
* Implementasi mudah, scalable, dan bisa dipasang di kendaraan modern
* Menjadi dasar untuk fitur IoV (Internet of Vehicle) tingkat lanjut

---

## 📂 **Dataset**

Dataset yang digunakan merupakan dataset wajah custom, terdiri dari:

### **1. Data Owner**

* Foto wajah pemilik (class: `"fat"`)
* Diambil dalam berbagai pencahayaan dan ekspresi
* Jumlah: ± 100–200 gambar
* Format: `.jpg`

### **3. Labeling**

* Dilakukan dengan **LabelImg**
* Label: `fat` (owner)

Dataset kemudian di-convert ke format YOLO (`.txt` per image).

---

## 🧠 **Model**

Model yang digunakan pada sistem ini:

### **✨ YOLOv8 Custom Training**

* Base model: `YOLOv8n` atau `YOLOv8s`
* Task: Face detection & classification
* Training dilakukan menggunakan *Ultralytics YOLO*
* Output model disimpan pada:

  ```
  runs/detect/train7/weights/best.pt
  ```

### **Hyperparameters**

* Confidence filter: `0.25`
* Owner threshold: `0.75`
  → Jika wajah terdeteksi sebagai owner tetapi confidence < 0.75, dianggap stranger (*fail-safe mode*).

---

## 📈 **Model Performance (Metrics)**
<img width="2400" height="1200" alt="results" src="https://github.com/user-attachments/assets/aa54c36a-08ec-4d52-bff0-c1fef8d69d99" />


![val_batch1_pred](https://github.com/user-attachments/assets/bfd6d58c-ea42-4ae2-866e-a55e4ed5de62)


<img width="3000" height="2250" alt="confusion_matrix" src="https://github.com/user-attachments/assets/d9af6029-2cd2-4c35-8f45-b56e0b0b59f0" />

```

---

## 🔧 **System Flow**

**Input → Process → Output**

1. Webcam menangkap gambar pengemudi
2. YOLO mendeteksi wajah dan mengklasifikasikan sebagai:

   * **Owner** (label = fat, conf ≥ 0.75)
   * **Stranger** (label ≠ fat, atau conf < threshold)
3. Jika stranger terdeteksi:

   * Capture frame wajah
   * Kirim **notifikasi Telegram**
   * Kirim **foto realtime** ke Telegram
4. Sistem menampilkan bounding box warna:

   * **Hijau → Owner**
   * **Merah → Stranger**

---

## 📬 **Telegram Integration**

Sistem mengirimkan alert melalui Telegram:

* Pesan teks berisi:

  * label prediksi
  * confidence
  * timestamp
* Foto wajah stranger yang tertangkap kamera
* Cooldown notifikasi: **5 detik** (untuk menghindari spam)

---

## 🏁 **Kesimpulan**

Project Anti-Theft Driver Recognition ini berhasil menunjukkan bahwa:

* Identifikasi pengemudi berbasis Computer Vision efektif untuk mendeteksi orang asing
* Sistem ini dapat berjalan real-time bahkan dengan hardware sederhana (webcam + laptop)
* Integrasi Telegram meningkatkan respons cepat terhadap potensi pencurian
* Custom training YOLO memberikan akurasi baik untuk kasus single-user owner

Sistem ini dapat dikembangkan lebih lanjut untuk:

* Integrasi dengan CAN Bus untuk memblok starting engine
* Menyimpan log ke cloud
* Multi-owner recognition
* Integrasi ke IoV ecosystem


✅ Tambahin **diagram arsitektur** (teks / ASCII)
✅ Buatkan **flowchart**
✅ Tambahkan **contoh gambar**
✅ Auto-generate README + folder structure (siap upload GitHub)

Mau ditambahin yang mana, Tom?
