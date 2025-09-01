from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from resume_analyzer import ResumeAnalyzer
from cover_letter_generator import CoverLetterGenerator
import json

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            return jsonify({
                'message': 'Resume uploaded successfully',
                'filename': filename,
                'filepath': filepath
            })
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    try:
        data = request.get_json()
        resume_path = data.get('resume_path')
        job_description = data.get('job_description')
        
        if not resume_path or not job_description:
            return jsonify({'error': 'Resume path and job description are required'}), 400
        
        analyzer = ResumeAnalyzer()
        analysis_result = analyzer.analyze_resume(resume_path, job_description)
        
        return jsonify(analysis_result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    try:
        data = request.get_json()
        resume_path = data.get('resume_path')
        job_description = data.get('job_description')
        company_name = data.get('company_name', '')
        position_title = data.get('position_title', '')
        
        if not resume_path or not job_description:
            return jsonify({'error': 'Resume path and job description are required'}), 400
        
        generator = CoverLetterGenerator()
        cover_letter = generator.generate_cover_letter(
            resume_path, 
            job_description, 
            company_name, 
            position_title
        )
        
        return jsonify({'cover_letter': cover_letter})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
