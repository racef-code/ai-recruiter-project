from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit as st
from typing import Optional, List, Dict, Any

try:
    from config import config
    from logger import logger
except ImportError:
    # Fallback if config/logger not available
    config = None
    logger = None


@st.cache_resource(show_spinner="Loading embedding model...")
def get_model(model_name: Optional[str] = None) -> SentenceTransformer:
    """
    Load and cache the SentenceTransformer model.

    Uses Streamlit's cache_resource to ensure the model is:
    - Loaded only once per app lifecycle
    - Shared across all sessions
    - Persists across reruns

    Args:
        model_name: Name of the model to load (defaults to config value)

    Returns:
        Loaded SentenceTransformer model
    """
    if config:
        model_name = model_name or config.model.name
        cache_dir = config.model.cache_dir
        device = config.model.device
    else:
        model_name = model_name or 'all-MiniLM-L6-v2'
        cache_dir = None
        device = 'cpu'

    if logger:
        logger.info(f"Loading SentenceTransformer model: {model_name}")

    try:
        model = SentenceTransformer(
            model_name,
            cache_folder=cache_dir,
            device=device
        )
        if logger:
            logger.info(f"Model loaded successfully: {model_name}")
        return model
    except Exception as e:
        if logger:
            logger.error(f"Failed to load model {model_name}: {e}", exc_info=True)
        raise

def get_embeddings(text_list: list):
    """
    Converts a list of strings into a matrix of vectors.

    Args:
        text_list: List of text strings to embed

    Returns:
        numpy array of embeddings
    """
    model = get_model()
    if logger:
        logger.debug(f"Generating embeddings for {len(text_list)} texts")
    embeddings = model.encode(text_list)
    return embeddings

def rank_resumes(job_description: str, resumes: list):
    """
    Ranks resumes by similarity to job description using cosine similarity.

    Steps:
    1. Vectorizes the Job Description
    2. Vectorizes all Resumes
    3. Calculates Cosine Similarity
    4. Returns a sorted list of matches

    Args:
        job_description: The job posting text
        resumes: List of dicts with 'filename' and 'content' keys

    Returns:
        List of dicts with 'filename', 'score', and 'content', sorted by score descending
    """
    model = get_model()

    if logger:
        logger.info(f"Ranking {len(resumes)} resumes against job description")

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

    if logger and results:
        logger.info(f"Ranking complete. Top score: {results[0]['score']:.4f}")

    return results