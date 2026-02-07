import json
import os
from typing import Dict, List, Optional, Any
import random

class QuestionManager:
    """Manages question bank and selection."""
    
    def __init__(self, question_bank_path: str = None):
        self.question_bank_path = question_bank_path or os.path.join(
            os.path.dirname(__file__), 'question_bank.json'
        )
        self.questions = self._load_questions()
    
    def _load_questions(self) -> Dict[str, Dict[str, List[Dict]]]:
        """Load question bank from JSON file."""
        try:
            with open(self.question_bank_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Question bank not found: {self.question_bank_path}")
    
    def get_question(self, role: str, difficulty: str, question_id: str = None) -> Optional[Dict[str, Any]]:
        """Get a specific question or random question for role/difficulty."""
        try:
            questions = self.questions[role][difficulty]
            
            if question_id:
                for q in questions:
                    if q['id'] == question_id:
                        return q.copy()
                return None
            
            return random.choice(questions).copy() if questions else None
        except KeyError:
            return None
    
    def get_questions_for_role_difficulty(self, role: str, difficulty: str) -> List[Dict[str, Any]]:
        """Get all questions for a role and difficulty level."""
        try:
            questions = self.questions[role][difficulty]
            return [q.copy() for q in questions]
        except KeyError:
            return []
    
    def get_all_difficulties_for_role(self, role: str) -> List[str]:
        """Get all difficulty levels for a role."""
        if role in self.questions:
            return list(self.questions[role].keys())
        return []
    
    def get_available_roles(self) -> List[str]:
        """Get all roles in question bank."""
        return list(self.questions.keys())
    
    def validate_question(self, role: str, difficulty: str) -> bool:
        """Check if role/difficulty combination exists."""
        return role in self.questions and difficulty in self.questions[role]
   
    def get_questions(self, role, domain, experience_level, count=5):
        import json
        import os

        questions_path = os.path.join(os.path.dirname(__file__), "question_bank.json")
        with open(questions_path, "r") as f:
            all_questions = json.load(f)

        filtered = []
        for q in all_questions:
            # If q is a string, wrap it as a dict
            if isinstance(q, str):
                filtered.append({"text": q})
            # If q is a dict, filter by role/domain/experience_level
            elif isinstance(q, dict):
                if (
                    (not q.get("role") or q.get("role") == role) and
                    (not q.get("domain") or q.get("domain") == domain) and
                    (not q.get("experience_level") or q.get("experience_level") == experience_level)
                ):
                    filtered.append(q)
        return filtered[:count]
        return filtered[:count]
