# Resume + Cover Letter Assistant

A powerful web application that helps job seekers analyze their resume against job descriptions and automatically generate personalized cover letters using NLP techniques.

## Features

### 🔍 Resume Analysis
- **File Support**: Upload resumes in PDF, DOCX, DOC, or TXT formats
- **Match Score**: Get a percentage score showing how well your resume matches the job description
- **Missing Keywords**: Identify important keywords from the job description that are missing from your resume
- **Skills Analysis**: Detailed breakdown of skills match by category (programming, databases, frameworks, etc.)
- **Smart Recommendations**: Get actionable advice to improve your resume

### ✉️ Cover Letter Generation
- **Personalized Content**: Automatically generates cover letters based on your resume and the job description
- **NLP-Powered**: Uses natural language processing to extract relevant skills and experience
- **Professional Format**: Properly formatted cover letters with your contact information
- **Download Options**: Copy to clipboard or download as text file

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## Usage

### Step 1: Upload Resume
1. Click on the upload area or drag and drop your resume file
2. Supported formats: PDF, DOCX, DOC, TXT
3. Wait for the upload confirmation

### Step 2: Enter Job Description
1. Optionally enter the company name and position title
2. Paste the complete job description in the text area
3. Click "Analyze Resume" to get insights

### Step 3: Review Analysis
- View your match score (0-100%)
- Check missing keywords that you should add to your resume
- Review skills analysis by category
- Read personalized recommendations

### Step 4: Generate Cover Letter
1. Click "Generate Cover Letter" to create a personalized cover letter
2. Review the generated content
3. Copy to clipboard or download as text file

## Technical Details

### Backend Technologies
- **Flask**: Web framework for the API
- **NLTK**: Natural language processing for text analysis
- **scikit-learn**: Machine learning for similarity scoring
- **PyPDF2**: PDF text extraction
- **python-docx2txt**: DOCX text extraction

### Key Algorithms
- **TF-IDF Vectorization**: For calculating document similarity
- **Cosine Similarity**: For measuring resume-job description match
- **Keyword Extraction**: Using NLTK for identifying important terms
- **Skills Categorization**: Predefined categories for technical and soft skills

### File Structure
```
resume-cover-letter-assistant/
├── app.py                 # Main Flask application
├── resume_analyzer.py     # Resume analysis logic
├── cover_letter_generator.py  # Cover letter generation
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Frontend interface
├── uploads/              # Uploaded resume files
└── README.md            # This file
```

## API Endpoints

### POST /upload-resume
Upload a resume file (PDF, DOCX, DOC, TXT)

### POST /analyze-resume
Analyze resume against job description
```json
{
  "resume_path": "path/to/resume.pdf",
  "job_description": "Job description text..."
}
```

### POST /generate-cover-letter
Generate personalized cover letter
```json
{
  "resume_path": "path/to/resume.pdf",
  "job_description": "Job description text...",
  "company_name": "Company Name",
  "position_title": "Position Title"
}
```

## Customization

### Adding New Skills Categories
Edit the `skills_keywords` dictionary in `resume_analyzer.py`:

```python
self.skills_keywords = {
    'your_category': ['skill1', 'skill2', 'skill3'],
    # ... existing categories
}
```

### Modifying Cover Letter Templates
Edit the `templates` dictionary in `cover_letter_generator.py`:

```python
self.templates = {
    'opening': [
        "Your custom opening template {position} at {company}...",
        # ... more templates
    ],
    # ... other sections
}
```

## Troubleshooting

### Common Issues

1. **NLTK Data Not Found**
   - The application automatically downloads required NLTK data
   - If issues persist, manually download:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

2. **File Upload Errors**
   - Ensure file is in supported format (PDF, DOCX, DOC, TXT)
   - Check file size (recommended < 10MB)
   - Verify file is not corrupted

3. **Analysis Errors**
   - Ensure job description is not empty
   - Check that resume file was uploaded successfully
   - Verify resume contains readable text

### Performance Tips
- For large job descriptions, consider breaking them into smaller sections
- Resume files should be text-based for best results
- Close other applications to free up memory if processing is slow

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Improving the UI/UX
- Adding new skills categories
- Enhancing the NLP algorithms

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Review the error messages in the browser console
3. Check the Flask application logs for backend errors

---

**Happy job hunting! 🚀**
