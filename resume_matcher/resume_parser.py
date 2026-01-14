import pypdf
from typing import List, Dict

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Opens a PDF file and extracts text from all pages.
    """
    text = ""
    try:
        reader = pypdf.PdfReader(pdf_path)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""
    
    return text.strip()

def load_resumes(file_paths: List[str]) -> List[Dict]:
    """
    Iterates through a list of file paths and returns a structured list 
    of dictionaries containing the filename and the extracted text.
    """
    resume_data = []
    
    for path in file_paths:
        text = extract_text_from_pdf(path)
        if text:
            resume_data.append({
                "filename": path,
                "content": text
            })
            
    return resume_data