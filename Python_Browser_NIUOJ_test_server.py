import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'log'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        # 獲取當前時間並格式化為 yyyymmddhhmmss
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        # 將時間戳記加入檔名
        filename = secure_filename(f'{timestamp}_status.log')
        
        # 獲取上傳者的IP地址
        uploader_ip = request.remote_addr
        # 檢查IP地址是否符合特定格式（例如：192.168.6.X）
        if uploader_ip.startswith('192.168.6.'):
            # 從IP地址中提取最後一個段
            ip_segment = uploader_ip.split('.')[-1]
            # 創建一個基於IP段的資料夾名稱
            upload_folder = f'./uploads/{ip_segment}'
            # 如果資料夾不存在，則創建它
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            # 保存檔案到指定的資料夾
            file.save(os.path.join(upload_folder, filename))
            return jsonify({'message': 'File successfully uploaded'}), 200
        else:
            return jsonify({'message': 'Invalid IP address'}), 400
    else:
        return jsonify({'message': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(host='192.168.6.2', port=8000)
