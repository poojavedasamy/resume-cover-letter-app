import PyPDF2
import docx2txt
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

# Download required NLTK data
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
        self.skills_keywords = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server'],
            'frameworks': ['django', 'flask', 'react', 'angular', 'vue', 'node.js', 'express', 'spring', 'laravel'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins'],
            'tools': ['git', 'github', 'gitlab', 'jira', 'confluence', 'slack', 'trello'],
            'methodologies': ['agile', 'scrum', 'kanban', 'waterfall', 'devops', 'ci/cd'],
            'soft_skills': ['leadership', 'communication', 'teamwork', 'problem solving', 'time management']
        }
    
    def extract_text_from_file(self, file_path):
        """Extract text from PDF, DOCX, or TXT files"""
        file_extension = file_path.lower().split('.')[-1]
        
        try:
            if file_extension == 'pdf':
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    return text
            
            elif file_extension in ['docx', 'doc']:
                return docx2txt.process(file_path)
            
            elif file_extension == 'txt':
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
                
        except Exception as e:
            raise Exception(f"Error extracting text from file: {str(e)}")
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_keywords(self, text):
        """Extract keywords from text"""
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stop words and short words
        keywords = [word for word in tokens if word not in self.stop_words and len(word) > 2]
        
        # Extract skills
        skills_found = {}
        for category, skill_list in self.skills_keywords.items():
            found_skills = [skill for skill in skill_list if skill in text.lower()]
            if found_skills:
                skills_found[category] = found_skills
        
        return keywords, skills_found
    
    def calculate_similarity(self, resume_text, job_description):
        """Calculate similarity between resume and job description"""
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        
        # Combine texts for fitting
        combined_texts = [resume_text, job_description]
        tfidf_matrix = vectorizer.fit_transform(combined_texts)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return similarity
    
    def find_missing_keywords(self, resume_text, job_description):
        """Find keywords in job description that are missing from resume"""
        # Extract keywords from job description
        job_keywords, _ = self.extract_keywords(job_description)
        
        # Extract keywords from resume
        resume_keywords, _ = self.extract_keywords(resume_text)
        
        # Find missing keywords
        missing_keywords = []
        for keyword in job_keywords:
            if keyword not in resume_keywords and len(keyword) > 3:
                missing_keywords.append(keyword)
        
        # Remove duplicates and limit to top 20
        missing_keywords = list(set(missing_keywords))[:20]
        
        return missing_keywords
    
    def analyze_resume(self, resume_path, job_description):
        """Main analysis function"""
        try:
            # Extract text from resume
            resume_text = self.extract_text_from_file(resume_path)
            
            # Preprocess texts
            clean_resume = self.preprocess_text(resume_text)
            clean_job_desc = self.preprocess_text(job_description)
            
            # Extract keywords and skills
            resume_keywords, resume_skills = self.extract_keywords(clean_resume)
            job_keywords, job_skills = self.extract_keywords(clean_job_desc)
            
            # Calculate similarity score
            similarity_score = self.calculate_similarity(clean_resume, clean_job_desc)
            match_score = round(similarity_score * 100, 2)
            
            # Find missing keywords
            missing_keywords = self.find_missing_keywords(clean_resume, clean_job_desc)
            
            # Analyze skills match
            skills_analysis = {}
            for category in self.skills_keywords.keys():
                resume_skills_in_category = resume_skills.get(category, [])
                job_skills_in_category = job_skills.get(category, [])
                
                if job_skills_in_category:
                    matched_skills = [skill for skill in job_skills_in_category if skill in resume_skills_in_category]
                    skills_analysis[category] = {
                        'required': job_skills_in_category,
                        'found': matched_skills,
                        'missing': [skill for skill in job_skills_in_category if skill not in resume_skills_in_category],
                        'match_percentage': round(len(matched_skills) / len(job_skills_in_category) * 100, 2) if job_skills_in_category else 0
                    }
            
            # Generate recommendations
            recommendations = []
            if match_score < 70:
                recommendations.append("Consider adding more relevant keywords from the job description to your resume.")
            
            if missing_keywords:
                recommendations.append(f"Add these keywords to your resume: {', '.join(missing_keywords[:10])}")
            
            for category, analysis in skills_analysis.items():
                if analysis['match_percentage'] < 50:
                    recommendations.append(f"Focus on adding more {category} skills to your resume.")
            
            return {
                'match_score': match_score,
                'missing_keywords': missing_keywords,
                'skills_analysis': skills_analysis,
                'recommendations': recommendations,
                'resume_keywords_count': len(resume_keywords),
                'job_keywords_count': len(job_keywords),
                'resume_skills': resume_skills,
                'job_skills': job_skills
            }
            
        except Exception as e:
            raise Exception(f"Error analyzing resume: {str(e)}")
