import logging
import json
import requests
from decouple import config

FIREWORKS_API_KEY = config("FIREWORKS_API_KEY", default=None)
FIREWORKS_BASE_URL = config("FIREWORKS_BASE_URL", default="https://api.fireworks.ai/inference/v1")

def generate_text_fireworks(prompt, system_prompt="You are a helpful AI assistant."):
    if not FIREWORKS_API_KEY:
        return "Error: Fireworks API key not configured."
    
    # Use a default model if not configured specifically for chat
    model = "accounts/fireworks/models/llama-v3p1-70b-instruct"
    
    url = f"{FIREWORKS_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1024,
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error generating text: {str(e)}"

logger = logging.getLogger(__name__)

class CodingProfileAnalysisService:
    @staticmethod
    def analyze_profile(profile):
        """
        Generates an AI analysis of the user's coding profile stats.
        """
        stats = profile.stats
        platform = profile.platform
        
        if not stats:
            return None

        prompt = f"""
        You are an expert technical interviewer and career coach.
        Analyze the following {platform} statistics for a job seeker:
        
        {json.dumps(stats, indent=2)}
        
        The stats include advanced metrics like:
        - Weighted Acceptance Rate (accounts for problem difficulty)
        - Consistency (streaks, weekly average)
        - Problem Solving Score (0-100 unified score)
        - Community Engagement
        
        Provide a constructive analysis in JSON format with the following keys:
        - "summary": A brief 1-2 sentence summary of their skill level.
        - "strengths": A list of 2-3 key strengths based on the data.
        - "weaknesses": A list of 2-3 areas for improvement.
        - "recommendations": A list of 2-3 specific actions to take next (e.g., "Practice dynamic programming", "Participate in more contests").
        - "estimated_level": One of "Beginner", "Intermediate", "Advanced", "Expert".
        - "insights": A list of 2-3 short, punchy insights (e.g., "Strong consistency with moderate difficulty", "High volume but low acceptance rate").
        
        Do not include any markdown formatting or explanations outside the JSON.
        """

        try:
            # Using the existing generate_text_fireworks function from rag.py
            # We might need to adjust if it returns markdown code blocks
            response_text = generate_text_fireworks(prompt, system_prompt="You are a helpful JSON-speaking assistant.")
            
            # Clean up potential markdown code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
                
            analysis = json.loads(response_text)
            return analysis

        except Exception as e:
            logger.error(f"Error generating analysis for profile {profile.id}: {str(e)}")
            return None
