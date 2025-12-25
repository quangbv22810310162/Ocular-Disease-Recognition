
# Ocular Disease Recognition 🚀

Dự án nhận diện bệnh võng mạc (**Ocular Disease**) sử dụng mô hình Deep Learning giúp phân loại hình ảnh retina thành các lớp bệnh khác nhau. Đây là một project học tập / đồ án chuyên ngành Computer Vision.

---

## 🧠 Mục tiêu

- Xây dựng mô hình ML/DL phân loại bệnh mắt
- Huấn luyện và đánh giá mô hình
- Hiển thị kết quả đánh giá (accuracy, confusion matrix, ...)
- Làm quen pipeline xử lý ảnh, dataset, training và inferencing

---

## 📦 Công nghệ & thư viện

**Ngôn ngữ & Framework**
- Python 3.x

**Deep Learning**
- TensorFlow / Keras hoặc PyTorch

**Xử lý ảnh**
- OpenCV
- Pillow

**Tiện ích**
- NumPy
- Matplotlib (visualization)
- scikit-learn

---

## 🗂 Cấu trúc thư mục

```

Ocular-Disease-Recognition/
├── data/                  # Nơi chứa dataset (không push dataset lớn)
├── models/                # Mô hình đã train
├── notebooks/             # Notebook thí nghiệm
├── src/                   # Source code chính
│   ├── train.py
│   ├── evaluate.py
│   └── utils.py
├── requirements.txt       # Thư viện Python
├── .gitignore
└── README.md

````

---

## 🛠 Hướng dẫn cài đặt & chạy

### 1️⃣ Tạo môi trường ảo
```bash
python -m venv venv
````

Kích hoạt:

```bash
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux
```

---

### 2️⃣ Cài dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Chuẩn bị dữ liệu

Dữ liệu nên được đặt trong thư mục `data/`, theo cấu trúc:

```
data/
├── train/
│   ├── normal/
│   ├── dr/
│   ├── glaucoma/
│   └── others/
└── test/
```

---

### 4️⃣ Train mô hình

Chạy lệnh:

```bash
python src/train.py --data_dir data/ --epochs 20
```

---

### 5️⃣ Đánh giá mô hình

```bash
python src/evaluate.py --model models/best_model.pth
```

---

## 📊 Kết quả mẫu

> (Có thể chèn ảnh kết quả training, biểu đồ loss/accuracy, confusion matrix ở đây)

---

## 📌 Ghi chú

* Đây là project ML/CV học tập, có thể tiếp tục mở rộng
* Nên lưu mô hình tốt nhất trong `models/`

---

## 🙋‍♂️ Tác giả

**Bùi Văn Quang**
Sinh viên Công nghệ Thông tin

