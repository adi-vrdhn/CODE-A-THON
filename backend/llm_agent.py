import json
import requests

class InterviewAgent:
    """LLM-powered interview agent using Ollama (local)"""

    def __init__(self, model_name="mistral"):
        self.api_url = "http://localhost:11434/api/generate"
        self.model = model_name

    def generate_followup(self, question, answer, question_context=""):
        prompt = f"""You are an expert technical interviewer. Based on the candidate's answer, generate ONE concise follow-up question.

Question: {question}
Candidate Answer: {answer}
Context: {question_context}

Generate a follow-up that:
1. Probes deeper into their understanding
2. Tests edge cases or advanced concepts
3. Is clear and specific

Respond with ONLY the follow-up question."""
        response = requests.post(self.api_url, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })
        return response.json()['response'].strip()

    def score_answer(self, question, answer, expected_concepts=None):
        if expected_concepts is None:
            expected_concepts = ["understanding", "approach"]

        prompt = f"""Score this technical answer 0-100.

Question: {question}
Answer: {answer}
Expected: {', '.join(expected_concepts)}

Evaluate clarity, accuracy, completeness, confidence (25% each).

Respond in JSON:
{{"score": <int>, "clarity": <int>, "accuracy": <int>, "completeness": <int>, "confidence": <int>, "feedback": "<string>"}}"""
        response = requests.post(self.api_url, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })
        try:
            return json.loads(response.json()['response'])
        except Exception:
            return {
                "score": 60,
                "clarity": 60,
                "accuracy": 60,
                "completeness": 60,
                "confidence": 60,
                "feedback": response.json()['response']
            }

    def generate_recommendations(self, answers, scores):
        avg_score = sum(s.get('score', 0) for s in scores) / len(scores) if scores else 0

        prompt = f"""Based on interview (avg score {avg_score:.0f}/100), give 3 actionable recommendations.

Respond in JSON:
{{"recommendations": ["rec1", "rec2", "rec3"]}}"""
        response = requests.post(self.api_url, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })
        try:
            return json.loads(response.json()['response'])
        except Exception:
            return {"recommendations": [response.json()['response']]}