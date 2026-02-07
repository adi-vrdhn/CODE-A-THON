from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
from questions.question_manager import QuestionManager
from scoring.scoring_engine import ScoringEngine

class InterviewEngine:
    """Core interview execution engine."""
    
    def __init__(self, config_manager, question_manager: QuestionManager):
        self.config = config_manager
        self.questions_mgr = question_manager
        self.scoring = ScoringEngine()
        self.interview_state = None
    
    def initialize_interview(self, candidate_info: Dict[str, str]) -> Dict[str, Any]:
        """
        Initialize a new interview.
        
        Args:
            candidate_info: {name, email, role, experience_level, domain}
        
        Returns:
            Interview session with first question
        """
        settings = self.config.get_interview_settings()
        
        self.interview_state = {
            'candidate': candidate_info,
            'started_at': datetime.now().isoformat(),
            'current_question_index': 0,
            'questions_answered': [],
            'results': [],
            'current_difficulty': self._get_starting_difficulty(candidate_info['experience_level']),
            'max_questions': settings.get('max_questions', 10),
            'status': 'in_progress'
        }
        
        # Get first question
        first_question = self._select_next_question(candidate_info['role'])
        
        return {
            'session_id': id(self),
            'candidate': candidate_info,
            'question': first_question,
            'question_number': 1,
            'total_questions': self.interview_state['max_questions']
        }
    
    def submit_answer(self, answer: str, follow_up_response: Optional[str] = None) -> Dict[str, Any]:
        """
        Submit and score an answer.
        
        Args:
            answer: Candidate's response to current question
            follow_up_response: Optional response to follow-up question
        
        Returns:
            Score result and next question (or completion if done)
        """
        if not self.interview_state or self.interview_state['status'] != 'in_progress':
            return {'error': 'No active interview'}
        
        current_idx = self.interview_state['current_question_index']
        current_question = self.interview_state['questions_answered'][current_idx]
        
        # Score the response
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'response_length': len(answer.split()),
            'has_follow_up': bool(follow_up_response),
            'follow_up_length': len(follow_up_response.split()) if follow_up_response else 0
        }
        
        score_result = self.scoring.score_response(answer, current_question, metadata)
        
        # Store result
        result_record = {
            'question_id': current_question['id'],
            'question_text': current_question['text'],
            'answer': answer,
            'follow_up_answer': follow_up_response,
            'follow_up_question': current_question.get('follow_up', ''),
            **score_result,
            'timestamp': metadata['timestamp']
        }
        
        self.interview_state['results'].append(result_record)
        
        # Adapt difficulty for next question
        self._adapt_difficulty(score_result['overall'])
        
        # Move to next question
        self.interview_state['current_question_index'] += 1
        
        # Check if interview is complete
        if self.interview_state['current_question_index'] >= self.interview_state['max_questions']:
            self.interview_state['status'] = 'completed'
            self.interview_state['completed_at'] = datetime.now().isoformat()
            
            return {
                'status': 'completed',
                'results': self.interview_state['results'],
                'message': 'Interview completed successfully'
            }
        
        # Get next question
        next_question = self._select_next_question(
            self.interview_state['candidate']['role']
        )
        
        self.interview_state['questions_answered'].append(next_question)
        
        return {
            'status': 'continuing',
            'result': result_record,
            'next_question': next_question,
            'question_number': self.interview_state['current_question_index'] + 1,
            'total_questions': self.interview_state['max_questions'],
            'scores_hidden': self.config.get_interview_settings().get('reveal_scores') == False
        }
    
    def _get_starting_difficulty(self, experience_level: str) -> str:
        """Determine starting difficulty based on experience level."""
        difficulty_map = {
            'Intern': 'Easy',
            'Junior': 'Easy',
            'Mid-level': 'Intermediate',
            'Senior': 'Hard',
            'Lead': 'Expert'
        }
        return difficulty_map.get(experience_level, 'Easy')
    
    def _select_next_question(self, role: str) -> Dict[str, Any]:
        """Select next question based on current difficulty."""
        question = self.questions_mgr.get_question(
            role,
            self.interview_state['current_difficulty']
        )
        
        if not question:
            # Fallback to available difficulty
            difficulties = self.questions_mgr.get_all_difficulties_for_role(role)
            if difficulties:
                question = self.questions_mgr.get_question(role, difficulties[0])
        
        self.interview_state['questions_answered'].append(question)
        return question
    
    def _adapt_difficulty(self, score: float):
        """Adapt next question difficulty based on current score."""
        difficulties = ['Easy', 'Intermediate', 'Hard', 'Expert']
        current_idx = difficulties.index(self.interview_state['current_difficulty'])
        
        # Score-based adaptation
        if score >= 4.5 and current_idx < len(difficulties) - 1:
            # Excellent - increase difficulty
            self.interview_state['current_difficulty'] = difficulties[current_idx + 1]
        elif score < 2.5 and current_idx > 0:
            # Poor - decrease difficulty
            self.interview_state['current_difficulty'] = difficulties[current_idx - 1]
        # else: maintain current difficulty
    
    def get_current_question(self) -> Optional[Dict[str, Any]]:
        """Get the current question."""
        if not self.interview_state:
            return None
        
        try:
            idx = self.interview_state['current_question_index']
            return self.interview_state['questions_answered'][idx]
        except (IndexError, KeyError):
            return None
    
    def get_interview_status(self) -> Dict[str, Any]:
        """Get current interview status."""
        if not self.interview_state:
            return {'status': 'no_interview'}
        
        return {
            'status': self.interview_state['status'],
            'candidate': self.interview_state['candidate'],
            'questions_completed': self.interview_state['current_question_index'],
            'total_questions': self.interview_state['max_questions'],
            'current_difficulty': self.interview_state['current_difficulty'],
            'started_at': self.interview_state['started_at'],
            'completed_at': self.interview_state.get('completed_at'),
            'results_count': len(self.interview_state['results'])
        }
    
    def get_results(self) -> List[Dict[str, Any]]:
        """Get all interview results."""
        if not self.interview_state:
            return []
        
        return self.interview_state['results']
