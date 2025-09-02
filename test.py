import os
import sys
from resume import ResumeAnalyzer
from cover_letter import CoverLetterGenerator
def test_resume_analyzer():
    print("🧪 Running Resume Analyzer Test...")
    res_path = "sample_resume.txt"
    job_path = "sample_job_description.txt"
    if not os.path.exists(res_path) or not os.path.exists(job_path):
        print("❌ Required sample files not found.")
        return False
    try:
        with open(job_path, 'r', encoding='utf-8') as f:
            job_desc = f.read()
        analyzer = ResumeAnalyzer()
        results = analyzer.analyze_resume(res_path, job_desc)
        if 'error' in results:
            print(f"❌ Analysis failed: {results['error']}")
            return False
        print("✅ Resume analysis completed.")
        print(f"Match Score: {results['match_score']}%")
        print(f"Missing Keywords: {', '.join(results['missing_keywords'][:5])}")
        return True
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return False
def test_cover_letter_generator():
    print("\n🧪 Running Cover Letter Generator Test...")
    res_path = "sample_resume.txt"
    job_path = "sample_job_description.txt"
    if not os.path.exists(res_path) or not os.path.exists(job_path):
        print("❌ Required sample files not found.")
        return False
    try:
        with open(job_path, 'r', encoding='utf-8') as f:
            job_desc = f.read()
        generator = CoverLetterGenerator()
        cover_letter = generator.generate_cover_letter(
            resume_path=res_path,
            job_description=job_desc,
            company_name="InnovativeTech Solutions",
            position_title="Senior Full-Stack Software Engineer"
        )   
        if cover_letter.startswith("Error"):
            print(f"❌ Generation failed: {cover_letter}")
            return False    
        print("✅ Cover letter generated.")
        print(f"Length: {len(cover_letter)} characters")
        return True
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return False
def run_tests():
    print("🚀 Starting Resume & Cover Letter Assistant Tests")
    print("=" * 60) 
    tests = [
        ("Resume Analyzer", test_resume_analyzer),
        ("Cover Letter Generator", test_cover_letter_generator)
    ]
    passed = 0
    total = len(tests)
    for name, func in tests:
        if func():
            print(f"✅ {name} PASSED\n")
            passed += 1
        else:
            print(f"❌ {name} FAILED\n")
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed.")
    if passed == total:
        print("🎉 All tests passed!")
        print("The application is ready to use.")
        return 0
    else:
        print("⚠️ Some tests failed. Please review the output above.")
        return 1
if __name__ == "__main__":
    sys.exit(run_tests())
