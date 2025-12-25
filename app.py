import os
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import tensorflow as tf
from PIL import Image
import numpy as np
from dotenv import load_dotenv

load_dotenv()

from chatbot import MedicalChatbot
from text_to_speech import TextToSpeech

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'please-set-a-secure-key')

# Cấu hình
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/uploads')
AUDIO_FOLDER = os.getenv('AUDIO_FOLDER', 'static/audio')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'jfif'}
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB default
DATABASE_PATH = os.getenv('DATABASE_PATH', 'database.db')
MODEL_PATH = os.getenv('MODEL_PATH', 'model/my_model.h5')
HOST = os.getenv('FLASK_HOST', '0.0.0.0')
PORT = int(os.getenv('FLASK_PORT', '5000'))
DEBUG_MODE = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

# Danh sách bệnh
DISEASES = ['Normal', 'Diabetes', 'Glaucoma', 'Cataract', 'AMD', 'Hypertension', 'Myopia', 'Others']

# Tải mô hình
model = tf.keras.models.load_model(MODEL_PATH)

chatbot = MedicalChatbot()
tts = TextToSpeech(audio_folder=app.config['AUDIO_FOLDER'])

def init_db():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT UNIQUE NOT NULL,
                     password TEXT NOT NULL)''')
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

def predict_disease(image_path):
    preprocessed_img = preprocess_image(image_path)
    predictions = model.predict(preprocessed_img)[0]
    results = [{'disease': disease, 'probability': float(prob)} for disease, prob in zip(DISEASES, predictions)]
    return sorted(results, key=lambda x: x['probability'], reverse=True)

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            c = conn.cursor()
            user = c.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                           (username, password)).fetchone()
            conn.close()
            
            if user:
                session['username'] = username
                return redirect(url_for('home'))
            else:
                error = 'Tài khoản hoặc mật khẩu không đúng'
        except Exception as e:
            error = f'Lỗi đăng nhập: {str(e)}'
    
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            error = 'Mật khẩu không khớp'
        else:
            try:
                conn = sqlite3.connect(DATABASE_PATH)
                c = conn.cursor()
                c.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username, password))
                conn.commit()
                conn.close()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                error = 'Tài khoản đã tồn tại'
            except Exception as e:
                error = f'Lỗi đăng ký: {str(e)}'
    
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    if 'file' not in request.files:
        return render_template('index.html', error='No file part')
    
    file = request.files['file']
    
    if file.filename == '':
        return render_template('index.html', error='No selected file')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            results = predict_disease(file_path)
            image_url = url_for('media_file', filename=filename)
            return render_template('result.html', results=results, image_url=image_url)
        except Exception as e:
            return render_template('index.html', error=f'Error processing file: {str(e)}')
    else:
        return render_template('index.html', error='File type not allowed')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/get_disease_info', methods=['POST'])
def get_disease_info():
    data = request.get_json()
    disease = data.get('disease')
    info_type = data.get('info_type')
    
    # Lấy thông tin từ chatbot
    info = chatbot.get_response(disease, info_type)
    
    # Tạo audio
    audio_file = tts.convert_to_speech(info)
    
    return jsonify({
        'info': info,
        'audio_url': url_for('audio_file', filename=audio_file)
    })


@app.route('/media/<path:filename>')
def media_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/audio/<path:filename>')
def audio_file(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename)

if __name__ == '__main__':
    init_db()
    app.run(host=HOST, port=PORT, debug=DEBUG_MODE)