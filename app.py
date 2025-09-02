from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from resume import ResumeAnalyzer
from cover_letter import CoverLetterGenerator
app = Flask(__name__)
CORS(app)
U_DIR = 'uploads'
EXTS = {'pdf', 'docx', 'doc', 'txt'}
app.config['UPLOAD_FOLDER'] = U_DIR
os.makedirs(U_DIR, exist_ok=True)
def ok_f(fn):
    return '.' in fn and fn.rsplit('.', 1)[1].lower() in EXTS
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/upload-resume', methods=['POST'])
def upload_r():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        f = request.files['resume']
        if f.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        if f and ok_f(f.filename):
            fn = secure_filename(f.filename)
            fp = os.path.join(a.config['UPLOAD_FOLDER'], fn)
            f.save(fp)
            return jsonify({'message': 'Resume uploaded successfully', 'filename': fn, 'filepath': fp})
        else:
            return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
