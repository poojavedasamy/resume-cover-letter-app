import os
import re
import PyPDF2
import docx2txt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
class ResumeAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.skills = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server'],
            'frameworks': ['django', 'flask', 'react', 'angular', 'vue', 'node.js', 'express', 'spring', 'laravel'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins'],
            'tools': ['git', 'github', 'gitlab', 'jira', 'confluence', 'slack', 'trello'],
            'methodologies': ['agile', 'scrum', 'kanban', 'waterfall', 'devops', 'ci/cd'],
            'soft_skills': ['leadership', 'communication', 'teamwork', 'problem solving', 'time management']
        }  
    def extract_text(self, p):
        """Extracts text from various file types."""
        ext = p.lower().split('.')[-1]
        try:
            if ext == 'pdf':
                with open(p, 'rb') as f:
                    r = PyPDF2.PdfReader(f)
                    t = ""
                    for page in r.pages:
                        t += page.extract_text()
                    return t
            elif ext in ['docx', 'doc']:
                return docx2txt.process(p)
            elif ext == 'txt':
                with open(p, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                raise ValueError(f"Unsupported file type: {ext}")
        except Exception as e:
            raise Exception(f"Error extracting text from file: {str(e)}")