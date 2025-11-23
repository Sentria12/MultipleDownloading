import os
from flask import Flask, request, send_from_directory, jsonify, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename
from functools import wraps

UPLOAD_DIRECTORY = "uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "X-API-Key"],
        "expose_headers": ["Content-Disposition"]
    }
})
app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY

# === BẢO MẬT: API Key ===
API_KEY = "123456"

def require_api_key(f):
    """Decorator kiểm tra API key"""
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

# === Endpoint 2: Lấy danh sách tệp ===
@app.route('/files', methods=['GET'])
@require_api_key  # Thêm bảo mật
def list_uploaded_files():
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        visible_files = [f for f in files if not f.startswith('.')]
        return jsonify(visible_files)
    except Exception as e:
        return make_response(jsonify(error=str(e)), 500)

# === Endpoint 3: Download 1 file ===
@app.route('/download/<path:filename>', methods=['GET'])
@require_api_key  # Thêm bảo mật
def serve_file(filename):
    try:
        # Decode URL encoding nếu cần
        from urllib.parse import unquote
        filename = unquote(filename)
        
        # Làm sạch tên file
        filename = safe_filename(filename)
        
        # Kiểm tra file có tồn tại
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return make_response(jsonify(error=f"Không tìm thấy tệp: {filename}"), 404)
        
        # Xác định MIME type dựa trên phần mở rộng
        import mimetypes
        mimetype = mimetypes.guess_type(filename)[0]
        
        print(f"Serving file: {filename}, mimetype: {mimetype}")
        
        return send_from_directory(
            app.config['UPLOAD_FOLDER'], 
            filename, 
            as_attachment=True,
            mimetype=mimetype
        )
    except FileNotFoundError:
        return make_response(jsonify(error="Không tìm thấy tệp"), 404)
    except Exception as e:
        print(f"Error serving file: {str(e)}")
        return make_response(jsonify(error=str(e)), 500)



if __name__ == '__main__':
    app.run(debug=True, port=5000)