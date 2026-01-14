from resume_matcher.resume_parser import load_resumes
from matcher import rank_resumes

# 1. Mock Data (Or replace with real PDF paths like ['cv1.pdf', 'cv2.pdf'])
# For this test, we will create dummy files, or just mock the output of the parser manually.
dummy_resumes = [
    {"filename": "Alice_Dev.pdf", "content": "Experienced Python developer with 5 years in Django and SQL."},
    {"filename": "Bob_Manager.pdf", "content": "Project manager skilled in Agile, Scrum, and team leadership."},
    {"filename": "Charlie_Data.pdf", "content": "Data Scientist expert in Python, Pandas, and Machine Learning."}
]

# 2. Define a Job Description
job_desc = "Looking for a Python expert to build backend systems using SQL."

print(f"--- Job: {job_desc} ---\n")

# 3. Run the Matcher
ranked_candidates = rank_resumes(job_desc, dummy_resumes)

# 4. Print Results
for candidate in ranked_candidates:
    print(f"Match: {candidate['score']:.4f} | File: {candidate['filename']}")
    # print(f"Preview: {candidate['content'][:50]}...")