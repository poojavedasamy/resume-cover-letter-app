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
    def preprocess(self, t):
        t = t.lower()
        t = re.sub(r'[^\w\s]', ' ', t)
        return re.sub(r'\s+', ' ', t).strip()
    
    def extract_kws(self, t):
        tokens = word_tokenize(t)
        kws = [w for w in tokens if w not in self.stop_words and len(w) > 2]
        s_found = {c: [s for s in sl if s in t] for c, sl in self.skills.items()}
        s_found = {k: v for k, v in s_found.items() if v}
        return kws, s_found
    
    def calc_sim(self, r_text, j_desc):
        v = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        c_texts = [r_text, j_desc]
        m = v.fit_transform(c_texts)
        return cosine_similarity(m[0:1], m[1:2])[0][0]
    
    def find_missing_kws(self, r_kws, j_kws):
        return list(set(j_kws) - set(r_kws))[:20]
    def analyze(self, r_path, j_desc):
        try:
            r_text = self.extract_text(r_path)
            c_res = self.preprocess(r_text)
            c_job = self.preprocess(j_desc)
            r_kws, r_skills = self.extract_kws(c_res)
            j_kws, j_skills = self.extract_kws(c_job)           
            sim = self.calc_sim(c_res, c_job)
            match_score = round(sim * 100, 2)            
            missing_kws = self.find_missing_kws(r_kws, j_kws)            
            s_ana = {}
            for cat, s_list in self.skills.items():
                j_s = j_skills.get(cat, [])
                r_s = r_skills.get(cat, [])
                if j_s:
                    m_s = [s for s in j_s if s in r_s]
                    s_ana[cat] = {
                        'required': j_s,
                        'found': m_s,
                        'missing': [s for s in j_s if s not in r_s],
                        'match_percentage': round(len(m_s) / len(j_s) * 100, 2) if j_s else 0
                    }            
            recs = []
            if match_score < 70:
                recs.append("Consider adding more keywords from the job description to your resume.")
            if missing_kws:
                recs.append(f"Add these keywords: {', '.join(missing_kws[:10])}")
            for cat, ana in s_ana.items():
                if ana['match_percentage'] < 50:
                    recs.append(f"Focus on adding more {cat} skills to your resume.")            
            return {
                'match_score': match_score,
                'missing_keywords': missing_kws,
                'skills_analysis': s_ana,
                'recommendations': recs,
                'resume_keywords_count': len(r_kws),
                'job_keywords_count': len(j_kws),
                'resume_skills': r_skills,
                'job_skills': j_skills
            }            
        except Exception as e:
            raise Exception(f"Error analyzing resume: {str(e)}")