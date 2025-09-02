from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from resume import ResumeAnalyzer
from cover_letter import CoverLetterGenerator

a = Flask(__name__)
CORS(a)

U_DIR = 'uploads'
EXTS = {'pdf', 'docx', 'doc', 'txt'}
a.config['UPLOAD_FOLDER'] = U_DIR

os.makedirs(U_DIR, exist_ok=True)

def ok_f(fn):
    return '.' in fn and fn.rsplit('.', 1)[1].lower() in EXTS

@a.route('/')
def home():
    return render_template('index.html')