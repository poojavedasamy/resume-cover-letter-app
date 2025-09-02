import re
import os
from datetime import datetime
from resume import ResumeAnalyzer

class CoverLetterGenerator:
    def __init__(self):
        self.anl = ResumeAnalyzer()
        self.tmpls = {
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