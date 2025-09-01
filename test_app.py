#!/usr/bin/env python3
import os
import sys
from resume_analyzer import ResumeAnalyzer
from cover_letter_generator import CoverLetterGenerator

def test_resume_analyzer():
    print("🧪 Testing Resume Analyzer...")
    
    # Check if sample files exist
    resume_path = "sample_resume.txt"
    job_path = "sample_job_description.txt"
    
    if not os.path.exists(resume_path):
        print(f"❌ Sample resume file not found: {resume_path}")
        return False
    
    if not os.path.exists(job_path):
        print(f"❌ Sample job description file not found: {job_path}")
        return False
    
    try:
        # Read job description
        with open(job_path, 'r', encoding='utf-8') as f:
            job_description = f.read()
        
        # Initialize analyzer
        analyzer = ResumeAnalyzer()
        
        # Analyze resume
        print("📊 Analyzing resume against job description...")
        results = analyzer.analyze_resume(resume_path, job_description)
        
        # Display results
        print(f"\n✅ Analysis completed successfully!")
        print(f"📈 Match Score: {results['match_score']}%")
        print(f"🔍 Missing Keywords: {len(results['missing_keywords'])} found")
        print(f"💡 Recommendations: {len(results['recommendations'])} provided")
        
        # Show some missing keywords
        if results['missing_keywords']:
            print(f"   Missing keywords: {', '.join(results['missing_keywords'][:5])}")
        
        # Show skills analysis
        if results['skills_analysis']:
            print(f"🎯 Skills Analysis:")
            for category, analysis in results['skills_analysis'].items():
                print(f"   {category}: {analysis['match_percentage']}% match")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during resume analysis: {str(e)}")
        return False

def test_cover_letter_generator():
    """Test the cover letter generator functionality"""
    print("\n🧪 Testing Cover Letter Generator...")
    
    resume_path = "sample_resume.txt"
    job_desc_path = "sample_job_description.txt"
    
    if not os.path.exists(resume_path) or not os.path.exists(job_path):
        print("❌ Sample files not found")
        return False
    
    try:
        # Read job description
        with open(job_path, 'r', encoding='utf-8') as f:
            job_description = f.read()
        
        # Initialize generator
        generator = CoverLetterGenerator()
        
        # Generate cover letter
        print("✉️ Generating cover letter...")
        cover_letter = generator.generate_cover_letter(
            resume_path=resume_path,
            job_description=job_description,
            company_name="InnovativeTech Solutions",
            position_title="Senior Full-Stack Software Engineer"
        )
        
        # Display results
        print(f"\n✅ Cover letter generated successfully!")
        print(f"📝 Length: {len(cover_letter)} characters")
        print(f"📄 Lines: {len(cover_letter.split(chr(10)))}")
        
        # Show preview
        print(f"\n📋 Cover Letter Preview:")
        print("-" * 50)
        lines = cover_letter.split(chr(10))
        for i, line in enumerate(lines[:10]):  # Show first 10 lines
            print(line)
        if len(lines) > 10:
            print("...")
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during cover letter generation: {str(e)}")
        return False

def test_file_extraction():
    """Test file text extraction functionality"""
    print("\n🧪 Testing File Text Extraction...")
    
    resume_path = "sample_resume.txt"
    
    if not os.path.exists(resume_path):
        print(f"❌ Sample resume file not found: {resume_path}")
        return False
    
    try:
        analyzer = ResumeAnalyzer()
        
        # Extract text
        print("📄 Extracting text from sample resume...")
        text = analyzer.extract_text_from_file(resume_path)
        
        # Analyze extraction
        print(f"✅ Text extraction successful!")
        print(f"📊 Text length: {len(text)} characters")
        print(f"📝 Lines: {len(text.split(chr(10)))}")
        
        # Check for key information
        key_info = {
            'name': 'John Doe' in text,
            'email': 'john.doe@email.com' in text,
            'phone': '(555) 123-4567' in text,
            'python': 'Python' in text,
            'javascript': 'JavaScript' in text,
            'experience': '5 years' in text
        }
        
        print(f"🔍 Key information found:")
        for key, found in key_info.items():
            status = "✅" if found else "❌"
            print(f"   {status} {key}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during text extraction: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Resume + Cover Letter Assistant Tests")
    print("=" * 60)
    
    tests = [
        ("File Text Extraction", test_file_extraction),
        ("Resume Analyzer", test_resume_analyzer),
        ("Cover Letter Generator", test_cover_letter_generator)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n{'='*60}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to use.")
        print("\n💡 To start the application:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Run the app: python app.py")
        print("   3. Open browser: http://localhost:5000")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
