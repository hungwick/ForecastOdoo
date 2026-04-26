# 📦 SMART INVENTORY FORECAST SYSTEM (ODOO)

## 📌 Giới thiệu

Hệ thống **Smart Inventory Forecast** là một module tùy chỉnh trên nền tảng Odoo, được xây dựng nhằm hỗ trợ doanh nghiệp nhỏ và vừa trong việc:

* Dự báo nhu cầu sản phẩm bằng AI
* Phân tích doanh thu theo thời gian
* Tính toán tiêu thụ nguyên liệu dựa trên BoM
* Đề xuất và tự động tạo đơn mua hàng

Hệ thống kết hợp giữa **Machine Learning (AI)** và **Business Logic**, giúp tối ưu hóa chuỗi cung ứng một cách đơn giản nhưng hiệu quả.

---

## 🎯 Mục tiêu hệ thống

* Dự báo mức nhu cầu (Low / Medium / High)
* Giảm tình trạng thiếu hoặc dư hàng
* Hỗ trợ ra quyết định nhập hàng
* Phân tích xu hướng bán hàng và nguyên liệu

---

## ⚙️ Kiến trúc hệ thống

Hệ thống gồm 3 thành phần chính:

### 1. 🤖 AI Model (Machine Learning)

* Thuật toán: Decision Tree Classifier
* Input:

  * Thứ trong tuần (weekday)
  * Tháng (month)
  * Cuối tuần (is_weekend)
* Output:

  * Nhóm nhu cầu: `Nhom_A`, `Nhom_B`, `Nhom_C`

---

### 2. 🧠 Business Logic

* Tính toán số lượng nhập:

  ```
  Required Qty = Base Qty + Safety Stock - Current Stock
  ```

* Làm tròn theo quy cách đóng gói

* Xử lý sản phẩm tươi (không lưu kho)

---

### 3. 🏢 Odoo System

* Lấy dữ liệu từ:

  * Sales
  * Product
  * BoM (Bill of Materials)
* Thực thi:

  * Forecast
  * Purchase Order
  * Dashboard

---

## 🚀 Chức năng chính

### 🔹 1. Dự báo nhu cầu (AI Forecast)

* Chạy mô hình AI để dự đoán nhu cầu
* Phân loại theo 3 mức:

  * Low (Nhom_A)
  * Medium (Nhom_B)
  * High (Nhom_C)

---

### 🔹 2. Đề xuất nhập hàng

* Tự động tính toán số lượng cần nhập
* Có thể chỉnh sửa trước khi tạo đơn mua
* Tránh nhập dư hoặc thiếu hàng

---

### 🔹 3. Tạo đơn mua hàng (Purchase Order)

* Tự động tạo PO từ forecast
* Liên kết với forecast để truy vết
* Đánh dấu đơn hàng do AI tạo

---

### 🔹 4. Phân tích doanh thu

* So sánh:

  * Hôm nay vs hôm qua
  * 7 ngày gần nhất vs 7 ngày trước
  * 30 ngày gần nhất vs 30 ngày trước

* Hiển thị xu hướng:

  * Tăng mạnh / Tăng / Giảm / Ổn định

---

### 🔹 5. Phân tích tiêu thụ nguyên liệu

* Tính toán dựa trên BoM
* Xác định:

  * Nguyên liệu tiêu thụ nhiều nhất
  * Xu hướng tăng/giảm

---

### 🔹 6. Dashboard & Visualization

* Giao diện trực quan
* Dễ theo dõi xu hướng kinh doanh

---

## 📊 Dataset & Training

### Dataset

* File: `dataset_3_years.csv`
* Dữ liệu mô phỏng trong 3 năm
* Bao gồm:

  * Ngày
  * Doanh số
  * Yếu tố thời gian

### Training

* File: `train_model.py`
* Thuật toán:

  * Decision Tree (entropy, max_depth=5)
* Output:

  * File model: `ai_model_universal.pkl`

---

## 📁 Cấu trúc thư mục

```
smart_inventory_forecast/
│
├── ai_training/
│   ├── dataset_3_years.csv
│   ├── generate_dataset.py
│   └── train_model.py
│
├── models/
│   ├── forecast_model.py
│   ├── sales_analytics.py
│   ├── material_usage.py
│   ├── product_template.py
│   └── purchase_order.py
│
├── views/
│   ├── forecast_view.xml
│   ├── sales_analytics_view.xml
│   ├── material_usage_view.xml
│   └── sales_dashboard.xml
│
├── security/
│   └── ir.model.access.csv
│
└── __manifest__.py
```

---

## 🛠️ Cài đặt

### 1. Clone project

```bash
git clone <repository_url>
```

### 2. Copy module vào Odoo addons

```bash
addons/smart_inventory_forecast/
```

### 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 4. Train model (nếu cần)

```bash
python ai_training/train_model.py
```

### 5. Restart Odoo & install module

---

## ▶️ Cách sử dụng

1. Vào menu **AI Forecast**
2. Tạo forecast mới
3. Chọn sản phẩm và ngày dự báo
4. Bấm **Run Forecast**
5. Xem:

   * Nhu cầu dự đoán
   * Số lượng đề xuất
6. Bấm **Create PO** để tạo đơn mua

---

## 📈 Kết quả đạt được

* Dự báo nhu cầu với độ chính xác tương đối (~85%)
* Tự động hóa quy trình nhập hàng
* Phân tích xu hướng bán hàng rõ ràng
* Hỗ trợ quyết định kinh doanh hiệu quả

---

## ⚠️ Hạn chế

* Mô hình AI còn đơn giản
* Chưa xử lý yếu tố mùa vụ phức tạp
* Chưa có dashboard nâng cao

---

## 🔮 Hướng phát triển

* Nâng cấp AI (Random Forest, LSTM)
* Bổ sung biểu đồ trực quan
* Tích hợp dữ liệu thời tiết, sự kiện
* Tối ưu hiệu năng

---

## 👨‍💻 Tác giả

* Sinh viên: Lương Mạnh Hùng
* Đề tài: Hệ thống dự báo nhu cầu và tối ưu chuỗi cung ứng trên nền tảng Odoo

---

## 📄 License

Dành cho mục đích học tập và nghiên cứu.
