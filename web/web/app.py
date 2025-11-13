import os
from flask import Flask, request, send_from_directory, jsonify, make_response
from flask_cors import CORS

UPLOAD_DIRECTORY = "../uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app = Flask(__name__)
CORS(app) 
app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY

@app.route('/files', methods=['GET'])
def list_uploaded_files():
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        visible_files = [f for f in files if not f.startswith('.')]
        return jsonify(visible_files)
    except Exception as e:
        return make_response(jsonify(error=str(e)), 500)

@app.route('/download/<path:filename>', methods=['GET'])
def serve_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return make_response(jsonify(error="Không tìm thấy tệp"), 404)

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
                os.remove(file_path)
                deleted_count += 1
            else:
                errors.append(f"Không tìm thấy: {filename}")
        except Exception as e:
            errors.append(f"Lỗi xóa {filename}: {str(e)}")

    if errors:
        return make_response(jsonify(success=f"Đã xóa {deleted_count} tệp", errors=errors), 207)
    
    return make_response(jsonify(success=f"Đã xóa {deleted_count} tệp"), 200)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
