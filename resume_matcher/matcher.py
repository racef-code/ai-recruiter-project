from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the model once to save time
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(text_list: list):
    """
    Converts a list of strings into a matrix of vectors.
    """
    embeddings = model.encode(text_list)
    return embeddings

def rank_resumes(job_description: str, resumes: list):
    """
    1. Vectorizes the Job Description.
    2. Vectorizes all Resumes.
    3. Calculates Cosine Similarity.
    4. Returns a sorted list of matches.
    """
    
    # 1. Get embedding for the job description
    # Reshape is needed because cosine_similarity expects a 2D array
    job_embedding = model.encode([job_description]) 
    
    # 2. Get embeddings for all resumes (just the content text)
    resume_texts = [r['content'] for r in resumes]
    resume_embeddings = model.encode(resume_texts)
    
    # 3. Calculate similarity
    # Result is a matrix of shape (1, n_resumes)
    scores = cosine_similarity(job_embedding, resume_embeddings)[0]
    
    # 4. Attach scores to resume objects and sort
    results = []
    for i, score in enumerate(scores):
        results.append({
            "filename": resumes[i]['filename'],
            "score": float(score), # Convert numpy float to python float
            "content": resumes[i]['content']
        })
    
    # Sort by score descending (highest match first)
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return results