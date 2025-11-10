import os
import zipfile
import io
from flask import Flask, request, send_from_directory, jsonify, make_response, send_file
from flask_cors import CORS

UPLOAD_DIRECTORY = "uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app = Flask(__name__)
# Cho phép trang web của bạn gọi đến server này
CORS(app) 
app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY

@app.route('/files', methods=['GET'])
def list_uploaded_files():
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        # Lọc ra các tệp ẩn (ví dụ: .DS_Store trên Mac)
        visible_files = [f for f in files if not f.startswith('.')]
        return jsonify(visible_files)
    except Exception as e:
        return make_response(jsonify(error=str(e)), 500)

# === Endpoint 3: Xử lý TẢI XUỐNG (Download 1 file) ===
@app.route('/download/<path:filename>', methods=['GET'])
def serve_file(filename):
    try:
        # Gửi tệp từ thư mục 'uploads' về máy client
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return make_response(jsonify(error="Không tìm thấy tệp"), 404)

# === ENDPOINT 4: Tải xuống nhiều file (ZIP) ===
@app.route('/download-multiple', methods=['POST'])
def download_multiple_files():
    data = request.get_json()
    filenames = data.get('files')

    if not filenames:
        return make_response(jsonify(error="Không có file nào được chọn"), 400)

    # Tạo một file ZIP "ảo" trong bộ nhớ
    memory_file = io.BytesIO()

    try:
        # Mở file ZIP để ghi
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filename in filenames:
                # Đường dẫn đầy đủ đến file
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if os.path.exists(file_path):
                    # Ghi file vào ZIP
                    # arcname=filename đảm bảo trong ZIP không bị lẫn lộn thư mục 'uploads/'
                    zf.write(file_path, arcname=filename)

        # Đưa con trỏ về đầu file "ảo"
        memory_file.seek(0)

        # Gửi file ZIP "ảo" này về cho người dùng
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name='download.zip' # Tên file zip khi tải về
        )
    except Exception as e:
        return make_response(jsonify(error=str(e)), 500)

# === ENDPOINT 5: Xóa nhiều file ===
@app.route('/delete', methods=['POST'])
def delete_multiple_files():
    data = request.get_json()
    filenames = data.get('files')

    if not filenames:
        return make_response(jsonify(error="Không có file nào được chọn"), 400)

    deleted_count = 0
    errors = []

    for filename in filenames:
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(file_path):
                os.remove(file_path) # Lệnh xóa file
                deleted_count += 1
            else:
                errors.append(f"Không tìm thấy tệp: {filename}")
        except Exception as e:
            errors.append(f"Lỗi khi xóa {filename}: {str(e)}")

    if errors:
        return make_response(jsonify(success=f"Đã xóa {deleted_count} tệp", errors=errors), 207) # 207 Multi-Status
    
    return make_response(jsonify(success=f"Đã xóa thành công {deleted_count} tệp"), 200)


if __name__ == '__main__':
    # Flask mặc định chạy ở cổng 5000
    app.run(debug=True, port=5000)