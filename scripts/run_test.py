import os
from resume_matcher.resume_parser import load_resumes
from resume_matcher.matcher import rank_resumes
from resume_matcher.explainer import generate_explanation

def main():
    # 1. Define where your PDFs are
    # This looks for all files ending in .pdf inside the 'data' folder
    data_folder = "data"
    pdf_files = [
        os.path.join(data_folder, f) 
        for f in os.listdir(data_folder) 
        if f.endswith('.pdf')
    ]

    if not pdf_files:
        print("❌ No PDFs found in the 'data' folder. Please add at least one PDF.")
        return

    print(f"📂 Found {len(pdf_files)} resumes: {pdf_files}")

    # 2. RUN PHASE 1: Parse the PDFs
    print("\n--- Phase 1: Parsing PDFs ---")
    resumes = load_resumes(pdf_files)
    
    # Check if text was actually extracted
    for res in resumes:
        preview = res['content'][:50].replace('\n', ' ')
        print(f"✅ Loaded: {res['filename']} (Length: {len(res['content'])} chars)")
        print(f"   Preview: \"{preview}...\"")

    # 3. RUN PHASE 2: Matching
    print("\n--- Phase 2: Matching ---")
    # A dummy job description for testing
    job_description = """
    We are looking for a Data Scientist with experience in Python, 
    Machine Learning, and Project Management.
    """
    
    ranked_results = rank_resumes(job_description, resumes)

    # 4. Display Results
    print(f"\n🎯 Job Description: {job_description.strip()}")
    print("-" * 40)
    print(f"{'SCORE':<10} | {'FILENAME'}")
    print("-" * 40)
    
    for result in ranked_results:
        print(f"{result['score']:.4f}     | {result['filename']}")

    # [NEW CODE] --- Phase 3: Generate Explanation ---
    print("\n--- Phase 3: LLM Explanation ---")
    
    # Let's take the top candidate (index 0)
    top_candidate = ranked_results[0]
    
    print(f"🥇 Top Candidate: {top_candidate['filename']} (Score: {top_candidate['score']:.4f})")
    print("⏳ Asking AI to explain (this may take a few seconds)...")
    
    explanation = generate_explanation(
        top_candidate['content'], 
        job_description
    )
    
    print("\n🤖 AI Recruiter Analysis:")
    print(explanation)

if __name__ == "__main__":
    main()