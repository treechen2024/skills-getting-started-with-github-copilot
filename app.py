from flask import Flask, render_template, request, jsonify
from google.generativeai import GenerativeModel, configure
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

app = Flask(__name__)

# 從環境變數獲取 API key
API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise ValueError("未設置 GEMINI_API_KEY 環境變數")

configure(api_key=API_KEY)
model = GenerativeModel('gemini-1.5-pro')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        prompt = request.json.get('prompt', '')
        if not prompt:
            return jsonify({'error': '請輸入提示語！'}), 400
        
        response = model.generate_content(prompt)
        return jsonify({'result': response.text})
    except Exception as e:
        return jsonify({'error': f'發生錯誤：{str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)