import os
from flask import Flask, request, send_from_directory, jsonify, make_response
from werkzeug.utils import secure_filename
from functools import wraps

UPLOAD_DIRECTORY = "uploads"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY

# === BẢO MẬT: API Key ===
API_KEY = "123456"
def require_api_key(f):
    """Decorator kiểm tra API key - CHỈ áp dụng cho API endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != API_KEY:
            return make_response(jsonify(error="Không có quyền truy cập"), 401)
        return f(*args, **kwargs)
    return decorated_function

def safe_filename(filename):
    """Làm sạch tên file để tránh path traversal"""
    filename = secure_filename(filename)
    filename = filename.replace('..', '')
    return filename

# ROUTES PHỤC VỤ FRONTEND

@app.route('/')
def serve_index():
    """Phục vụ trang chính"""
    print("Dang phuc vu index.html...")
    try:
        return send_from_directory('.', 'index.html')
    except Exception as e:
        print(f"Loi khi phuc vu index.html: {e}")
        return f"Loi: {str(e)}", 500

@app.route('/<path:filename>')
def serve_static(filename):
    """Phục vụ static files (CSS, JS, images)"""
    allowed_extensions = ['.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.txt']
    file_ext = os.path.splitext(filename)[1].lower()
    
    if file_ext in allowed_extensions:
        try:
            return send_from_directory('.', filename)
        except Exception as e:
            return make_response(jsonify(error=f"Không tìm thấy file: {filename}"), 404)
    else:
        return make_response(jsonify(error="File không được phép truy cập"), 403)

#Hàm định dạng dung lượng file
def get_file_size(file_path):
    """Lấy dung lượng file và trả về dạng bytes"""
    try:
        if os.path.exists(file_path):
            return os.path.getsize(file_path)
        return 0
    except OSError:
        return 0
    
def format_file_size(size_bytes):
    """Định dạng dung lượng file thành chuỗi dễ đọc"""
    if size_bytes is None or size_bytes == 0:
        return "0 B"
    
    try:
        size_bytes = int(size_bytes)  # Đảm bảo là số nguyên
    except (ValueError, TypeError):
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}"

# API ENDPOINTS (CÓ BẢO MẬT)

#API load files lên server
@app.route('/api/files', methods=['GET'])
@require_api_key
def list_uploaded_files():
    """Lấy danh sách file từ server kèm dung lượng"""
    try:
        print("Dang doc thu muc uploads...")
        files_info = []
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        visible_files = [f for f in files if not f.startswith('.')]
        
        for filename in visible_files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            size_bytes = get_file_size(file_path)
            files_info.append({
                'name': filename,
                'size_bytes': int(size_bytes),  # ĐẢM BẢO LÀ SỐ NGUYÊN
                'size_formatted': format_file_size(size_bytes)
            })
        
        print(f"Files tim thay: {[f['name'] for f in files_info]}")
        return jsonify(files_info)
    except Exception as e:
        print(f"Loi doc thu muc: {str(e)}")
        return make_response(jsonify(error=str(e)), 500)

#API tải file xuống
@app.route('/api/download/<path:filename>', methods=['GET'])
@require_api_key
def serve_file(filename):
    """Download file từ server"""
    try:
        # Decode URL encoding
        from urllib.parse import unquote
        filename = unquote(filename)
        
        # Làm sạch tên file
        filename = safe_filename(filename)
        
        # Kiểm tra file có tồn tại
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Dang tim file: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"File khong ton tai: {file_path}")
            available_files = os.listdir(app.config['UPLOAD_FOLDER'])
            print(f"Files co san: {available_files}")
            return make_response(jsonify(error=f"Không tìm thấy tệp: {filename}"), 404)
        
        # Xác định MIME type
        import mimetypes
        mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        
        print(f"Dang phuc vu file: {filename}, mimetype: {mimetype}")
        
        return send_from_directory(
            app.config['UPLOAD_FOLDER'], 
            filename, 
            as_attachment=True,
            mimetype=mimetype
        )
    except FileNotFoundError:
        return make_response(jsonify(error="Không tìm thấy tệp"), 404)
    except Exception as e:
        print(f"Loi khi phuc vu file {filename}: {str(e)}")
        return make_response(jsonify(error=str(e)), 500)

if __name__ == '__main__':
    print("Khoi dong Flask Server...")
    print(f"Working directory: {os.getcwd()}")
    print(f"Co file index.html: {'index.html' in os.listdir('.')}")
    print(f"Co thu muc uploads: {os.path.exists('uploads')}")
    print(f"Truy cap: http://127.0.0.1:5000") 
    app.run(debug=True, host='0.0.0.0', port=5000)
