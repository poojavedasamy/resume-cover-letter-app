import re
import os
from datetime import datetime
from resume_analyzer import ResumeAnalyzer

class CoverLetterGenerator:
    def __init__(self):
        self.analyzer = ResumeAnalyzer()
        self.templates = {
            'opening': [
                "I am writing to express my strong interest in the {position} position at {company}. With my background in {key_skills}, I am confident in my ability to contribute effectively to your team.",
                "I am excited to apply for the {position} role at {company}. My experience in {key_skills} aligns perfectly with the requirements of this position.",
                "I am writing to apply for the {position} position at {company}. My expertise in {key_skills} makes me an ideal candidate for this opportunity."
            ],
            'body': [
                "Throughout my career, I have demonstrated strong {key_skills} skills and a proven track record of {achievements}. I am particularly drawn to {company}'s commitment to {company_values} and believe my background would be valuable in achieving your goals.",
                "My experience includes {key_skills} and I have successfully {achievements}. I am impressed by {company}'s innovative approach to {industry_focus} and would welcome the opportunity to contribute to your continued success.",
                "With my background in {key_skills}, I have consistently {achievements}. I am excited about the possibility of joining {company} and contributing to your mission of {company_values}."
            ],
            'closing': [
                "I would welcome the opportunity to discuss how my skills and experience can benefit {company}. Thank you for considering my application. I look forward to hearing from you.",
                "I am confident that my background and enthusiasm would make me a valuable addition to your team. I would appreciate the opportunity to discuss this position further.",
                "Thank you for considering my application. I am excited about the possibility of contributing to {company}'s success and would welcome the chance to discuss this opportunity in person."
            ]
        }
    
    def extract_personal_info(self, resume_text):
        """Extract personal information from resume"""
        # Extract name (assuming it's at the beginning)
        lines = resume_text.split('\n')
        name = lines[0].strip() if lines else "Your Name"
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, resume_text)
        email = email_match.group() if email_match else "your.email@example.com"
        
        # Extract phone
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phone_match = re.search(phone_pattern, resume_text)
        phone = phone_match.group() if phone_match else "(555) 123-4567"
        
        return {
            'name': name,
            'email': email,
            'phone': phone
        }
    
    def extract_key_skills(self, resume_text, job_description):
        """Extract key skills that match between resume and job description"""
        # Use the analyzer to get skills
        clean_resume = self.analyzer.preprocess_text(resume_text)
        clean_job_desc = self.analyzer.preprocess_text(job_description)
        
        resume_keywords, resume_skills = self.analyzer.extract_keywords(clean_resume)
        job_keywords, job_skills = self.analyzer.extract_keywords(clean_job_desc)
        
        # Find matching skills
        matching_skills = []
        for category, skills in resume_skills.items():
            if category in job_skills:
                matching_skills.extend(skills)
        
        # Add matching keywords
        matching_keywords = [kw for kw in resume_keywords if kw in job_keywords and len(kw) > 3]
        matching_skills.extend(matching_keywords[:5])
        
        return list(set(matching_skills))[:8]  # Limit to 8 skills
    
    def generate_achievements(self, resume_text):
        """Generate achievement statements based on resume content"""
        achievements = [
            "delivering high-quality results in fast-paced environments",
            "collaborating effectively with cross-functional teams",
            "implementing innovative solutions to complex problems",
            "exceeding performance expectations and targets",
            "leading successful projects from conception to completion"
        ]
        
        # Look for specific achievements in resume
        achievement_keywords = ['achieved', 'increased', 'improved', 'developed', 'led', 'managed', 'created']
        for keyword in achievement_keywords:
            if keyword in resume_text.lower():
                achievements.append(f"successfully {keyword} various initiatives")
        
        return achievements[:3]
    
    def infer_company_values(self, job_description):
        """Infer company values from job description"""
        values_keywords = {
            'innovation': ['innovative', 'cutting-edge', 'technology', 'creative'],
            'collaboration': ['team', 'collaborative', 'partnership', 'cooperation'],
            'excellence': ['excellence', 'quality', 'best', 'outstanding'],
            'growth': ['growth', 'development', 'advancement', 'learning'],
            'customer_focus': ['customer', 'client', 'service', 'satisfaction']
        }
        
        job_desc_lower = job_description.lower()
        found_values = []
        
        for value, keywords in values_keywords.items():
            if any(keyword in job_desc_lower for keyword in keywords):
                found_values.append(value)
        
        return found_values[:2] if found_values else ['excellence', 'innovation']
    
    def infer_industry_focus(self, job_description):
        """Infer industry focus from job description"""
        industry_keywords = {
            'technology': ['software', 'technology', 'digital', 'tech', 'programming'],
            'healthcare': ['healthcare', 'medical', 'patient', 'clinical'],
            'finance': ['financial', 'banking', 'investment', 'accounting'],
            'education': ['education', 'teaching', 'learning', 'academic'],
            'marketing': ['marketing', 'advertising', 'brand', 'campaign']
        }
        
        job_desc_lower = job_description.lower()
        
        for industry, keywords in industry_keywords.items():
            if any(keyword in job_desc_lower for keyword in keywords):
                return industry
        
        return "business"
    
    def generate_cover_letter(self, resume_path, job_description, company_name="", position_title=""):
        """Generate a personalized cover letter"""
        try:
            # Extract text from resume
            resume_text = self.analyzer.extract_text_from_file(resume_path)
            
            # Extract personal information
            personal_info = self.extract_personal_info(resume_text)
            
            # Extract key skills
            key_skills = self.extract_key_skills(resume_text, job_description)
            key_skills_text = ', '.join(key_skills) if key_skills else "relevant skills"
            
            # Generate achievements
            achievements = self.generate_achievements(resume_text)
            achievements_text = ' and '.join(achievements)
            
            # Infer company values and industry focus
            company_values = self.infer_company_values(job_description)
            company_values_text = ' and '.join(company_values)
            
            industry_focus = self.infer_industry_focus(job_description)
            
            # Set defaults if not provided
            if not company_name:
                company_name = "your company"
            if not position_title:
                position_title = "the position"
            
            # Generate cover letter sections
            import random
            
            opening = random.choice(self.templates['opening']).format(
                position=position_title,
                company=company_name,
                key_skills=key_skills_text
            )
            
            body = random.choice(self.templates['body']).format(
                key_skills=key_skills_text,
                achievements=achievements_text,
                company=company_name,
                company_values=company_values_text,
                industry_focus=industry_focus
            )
            
            closing = random.choice(self.templates['closing']).format(
                company=company_name
            )
            
            # Format the complete cover letter
            cover_letter = f"""
{personal_info['name']}
{personal_info['email']}
{personal_info['phone']}

{datetime.now().strftime('%B %d, %Y')}

{company_name}

Dear Hiring Manager,

{opening}

{body}

{closing}

Sincerely,
{personal_info['name']}
"""
            
            return cover_letter.strip()
            
        except Exception as e:
            raise Exception(f"Error generating cover letter: {str(e)}")
    
    def generate_enhanced_cover_letter(self, resume_path, job_description, company_name="", position_title=""):
        """Generate an enhanced cover letter with more specific details"""
        try:
            # Get basic cover letter
            basic_letter = self.generate_cover_letter(resume_path, job_description, company_name, position_title)
            
            # Extract more specific information
            resume_text = self.analyzer.extract_text_from_file(resume_path)
            
            # Find years of experience
            experience_patterns = [
                r'(\d+)\s*years?\s*of\s*experience',
                r'experience:\s*(\d+)\s*years?',
                r'(\d+)\s*years?\s*in\s*the\s*field'
            ]
            
            years_experience = "several"
            for pattern in experience_patterns:
                match = re.search(pattern, resume_text.lower())
                if match:
                    years_experience = match.group(1)
                    break
            
            # Find specific technologies or tools
            tech_pattern = r'\b(python|java|javascript|react|angular|aws|docker|kubernetes|agile|scrum)\b'
            technologies = re.findall(tech_pattern, resume_text.lower())
            tech_text = ', '.join(set(technologies)) if technologies else "relevant technologies"
            
            # Enhance the cover letter
            enhanced_letter = basic_letter.replace(
                "relevant skills",
                f"{tech_text} and other relevant skills"
            )
            
            return enhanced_letter
            
        except Exception as e:
            raise Exception(f"Error generating enhanced cover letter: {str(e)}")
