
-----

# Ứng dụng Quản lý Tệp (Flask & Vanilla JS)

Đây là một ứng dụng web full-stack đơn giản, sử dụng **Flask (Python)** cho backend và **HTML/CSS/JavaScript (Vanilla JS)** cho frontend.

Ứng dụng này cho phép người dùng tải tệp lên server, xem danh sách tệp hiện có, tải xuống một hoặc nhiều tệp (dưới dạng ZIP), và xóa các tệp khỏi server.

## 🚀 Tính năng chính

  * **Tải lên (Upload):**
      * Hỗ trợ kéo-thả (drag-and-drop) hoặc chọn tệp qua cửa sổ duyệt.
      * Hiển thị thanh tiến trình (progress bar) khi tải lên.
      * Server tự động kiểm tra và từ chối nếu tệp đã tồn tại (trả về lỗi 409 Conflict).
  * **Tải xuống (Download):**
      * Hiển thị danh sách các tệp hiện có trên server với checkbox.
      * **Tải 1 tệp:** Nếu chỉ chọn 1 tệp, trình duyệt sẽ tải tệp đó với tên gốc.
      * **Tải nhiều tệp:** Nếu chọn 2 tệp trở lên, backend sẽ tự động nén chúng thành một file `download.zip` và cho phép tải về.
  * **Quản lý tệp:**
      * **Xóa tệp:** Cho phép chọn một hoặc nhiều tệp và xóa chúng khỏi server (có hộp thoại xác nhận).
      * **Làm mới:** Nút "Làm mới DS" để tải lại danh sách tệp từ server.
  * **Giao diện người dùng:**
      * Giao diện 2 tab rõ ràng (Tải xuống / Tải lên).
      * Hiển thị lịch sử các hành động (upload/download thành công, thất bại) và lưu vào LocalStorage của trình duyệt.
      * Nút "Xóa Lịch sử" để dọn dẹp thông báo.

## 🛠️ Công nghệ sử dụng

  * **Backend:** Python 3, Flask
  * **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS)
  * **API:** Sử dụng `XMLHttpRequest` (cho Upload) và `Fetch API` (cho Download/Delete/List).

## 📦 Cài đặt

Bạn cần có **Python 3** và **pip** đã được cài đặt trên máy.

1.  **Tạo thư mục dự án:**
    Đặt tất cả các tệp (`app.py`, `index.html`, `style.css`, `script.js`, `requirements.txt`, `.gitignore`) vào chung một thư mục.

2.  **Tạo và kích hoạt môi trường ảo:**
    Mở terminal (hoặc Command Prompt) trong thư mục dự án và chạy:

    ```bash
    # Tạo môi trường ảo (đặt tên là 'venv')
    python -m venv venv

    # Kích hoạt môi trường ảo
    # Trên Windows (cmd):
    .\venv\Scripts\activate

    # Trên macOS/Linux (bash):
    source venv/bin/activate
    ```

3.  **Cài đặt các gói phụ thuộc:**
    Khi môi trường ảo đã được kích hoạt, chạy lệnh sau để cài đặt các thư viện Python cần thiết từ file `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

## 🏃 Sử dụng

Ứng dụng gồm 2 phần (Backend và Frontend) cần được chạy song song.

### 1\. Chạy Backend (Server Flask)

Trong terminal (đã kích hoạt môi trường ảo), chạy file `app.py`:

```bash
python app.py
```

Bạn sẽ thấy thông báo server đang chạy, thường là ở địa chỉ `http://127.0.0.1:5000`:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
(Press CTRL+C to quit)
```

> **Lưu ý:** Server này sẽ tạo một thư mục tên là `uploads` trong thư mục dự án của bạn để chứa các tệp được tải lên.

### 2\. Mở Frontend (Giao diện người dùng)

Bạn không cần "chạy" file `index.html` qua server. Chỉ cần **nhấp đúp chuột vào file `index.html`** để mở nó bằng trình duyệt web (ví dụ: Chrome, Firefox, Edge).

Giao diện web (chạy từ `file:///.../index.html`) sẽ tự động kết nối đến server backend (đang chạy ở `http://127.0.0.1:5000`) nhờ đã cài đặt `flask-cors` trong `app.py`.

## 📁 Cấu trúc Thư mục

Đây là cấu trúc thư mục của dự án và giải thích các tệp:

```
/du-an-cua-ban
├── .gitignore          # Cấu hình Git bỏ qua thư mục 'venv'
├── app.py              # File chạy server backend (Flask)
├── index.html          # Giao diện người dùng (HTML)
[cite_start]├── requirements.txt    # Danh sách các thư viện Python [cite: 1]
├── script.js           # Logic xử lý của frontend (JavaScript)
├── style.css           # Định dạng giao diện (CSS)
└── uploads/            # (Thư mục này sẽ tự động được tạo khi chạy app.py)
```