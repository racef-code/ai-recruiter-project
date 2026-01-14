import requests
import json

def generate_explanation(resume_text: str, job_text: str) -> str:
    """
    Sends the resume and job description to the local Ollama instance 
    (running Llama 3) and returns a justification for the match.
    """
    
    # 1. Define the URL for Ollama's API
    url = "http://localhost:11434/api/generate"
    
    # 2. Construct the Prompt
    # Llama 3 responds well to clear, structured instructions.
    prompt = f"""
    You are an expert AI Technical Recruiter.
    
    JOB DESCRIPTION:
    {job_text}
    
    CANDIDATE RESUME:
    {resume_text[:4000]}
    
    TASK:
    Based on the resume content, explain in 3 concise bullet points why this candidate is a good match for the job.
    - Focus on matching hard skills (technologies) and relevant experience.
    - Do not hallucinate skills not present in the resume.
    """

    # 3. Prepare the Payload
    # NOTE: The model name here must match what you installed ("llama3")
    payload = {
        "model": "llama3", 
        "prompt": prompt,
        "stream": False,   # We want the full response at once
        "options": {
            "temperature": 0.7, # Controls creativity (0.7 is balanced)
            "num_ctx": 4096     # Context window size (memory)
        }
    }

    # 4. Send Request
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response generated.")
        else:
            return f"⚠️ Error {response.status_code}: {response.text}"
            
    except requests.exceptions.ConnectionError:
        return "⚠️ Error: Ollama is not running. Please launch the Ollama app."
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"