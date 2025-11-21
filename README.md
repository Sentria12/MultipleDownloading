# Ứng dụng Download Đa Luồng (Multi-thread Downloader)

Đây là ứng dụng mô phỏng hệ thống tải file đa luồng sử dụng **Flask (Python)** và **Vanilla JavaScript**. Ứng dụng tập trung vào kỹ thuật xử lý bất đồng bộ (Asynchronous) và giao diện tương tác Kéo-Thả (Drag & Drop).

## 🚀 Tính năng nổi bật 

1.  **Giao diện Kéo & Thả (Drag & Drop):**
    * Người dùng kéo file trực tiếp từ danh sách Server và thả vào vùng "Hàng đợi" (Queue) để chuẩn bị tải.
    * Hỗ trợ kéo file `.txt` chứa danh sách liên kết để tải hàng loạt.

2.  **Tải Đa Luồng (Multi-threading):**
    * Không nén file thành ZIP.
    * Mỗi file được tải trên một luồng kết nối riêng biệt (sử dụng `XMLHttpRequest` độc lập).
    * Có thể tải song song nhiều file cùng lúc mà không bị chặn (Non-blocking).

3.  **Theo dõi Thời gian thực (Real-time Monitoring):**
    * **Tiến độ:** Thanh Progress Bar chạy mượt mà cho từng file.
    * **Tốc độ:** Hiển thị tốc độ tải hiện tại (MB/s hoặc KB/s).
    * **Dung lượng:** Hiển thị dung lượng đã tải / Tổng dung lượng.

4.  **Quản lý Tác vụ:**
    * Hiển thị trạng thái: Đang tải, Hoàn tất, hoặc Lỗi.
    * Lưu lịch sử tải xuống ngay trên giao diện.

## 🛠️ Công nghệ sử dụng

* **Backend:** Python 3, Flask (Xử lý API liệt kê và gửi file).
* **Frontend:** HTML5, CSS3, JavaScript (Xử lý Logic đa luồng và Drag & Drop).
* **Giao thức:** HTTP/1.1 (GET method với Streaming response).

## 📦 Cài đặt & Chạy ứng dụng

### Bước 1: Chuẩn bị môi trường
Cài đặt Python 3 và các thư viện cần thiết:

```bash
pip install -r requirements.txt

````



### Bước 2: Khởi chạy Server

Mở terminal tại thư mục dự án và chạy lệnh:

```bash
python app.py
```

Server sẽ khởi động tại địa chỉ: `http://127.0.0.1:5000`

### Bước 3: Sử dụng Client

  * Mở file `index.html` bằng trình duyệt bất kỳ (Chrome, Edge, Firefox).
  * **Lưu ý:** Không cần chạy qua Live Server, có thể mở trực tiếp vì Backend đã hỗ trợ CORS.

## 📝 Hướng dẫn sử dụng

1.  **Chọn file:** Nhìn vào danh sách "File trên Server" bên trái.
2.  **Kéo thả:** Dùng chuột kéo tên file muốn tải và thả vào vùng ô vuông nét đứt (Drop Zone).
3.  **Tải xuống:** Nhấn nút "Tải đã chọn" để bắt đầu.
4.  **Quan sát:** Theo dõi tốc độ và tiến độ của từng file chạy song song ở bảng bên dưới.



```
