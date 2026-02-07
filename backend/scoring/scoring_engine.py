from typing import Dict, Any, List
import re
from datetime import datetime

class ScoringEngine:
    """Evaluates candidate responses on multiple dimensions."""
    
    def __init__(self):
        self.dimensions = ['clarity', 'accuracy', 'completeness', 'confidence']
    
    def score_response(self, 
                      response: str,
                      question: Dict[str, Any],
                      metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Score a response across all dimensions.
        
        Args:
            response: Candidate's answer
            question: Question dict with context/key_points
            metadata: Response metadata (timestamp, length, hesitations, etc.)
        
        Returns:
            Dict with per-dimension scores (1-5) and insights
        """
        metadata = metadata or {}
        
        scores = {
            'clarity': self._score_clarity(response, metadata),
            'accuracy': self._score_accuracy(response, question, metadata),
            'completeness': self._score_completeness(response, question, metadata),
            'confidence': self._score_confidence(response, metadata)
        }
        
        overall = sum(scores.values()) / len(scores)
        
        return {
            'scores': scores,
            'overall': overall,
            'insights': self._generate_insights(response, question, scores, metadata)
        }
    
    def _score_clarity(self, response: str, metadata: Dict[str, Any]) -> int:
        """
        Score clarity (1-5).
        Evaluates: organization, grammar, structure, ease of understanding.
        """
        if not response or len(response.strip()) == 0:
            return 1
        
        length = len(response.split())
        sentences = len(re.split(r'[.!?]+', response))
        avg_sentence_length = length / max(sentences, 1)
        
        # Check for coherence indicators
        transition_words = ['however', 'therefore', 'also', 'additionally', 'moreover', 'furthermore']
        has_transitions = any(word in response.lower() for word in transition_words)
        
        # Scoring logic
        score = 3  # baseline
        
        if length < 20:
            score -= 2  # too brief
        elif length > 300:
            score += 1  # adequately detailed
        
        if 10 < avg_sentence_length < 30:
            score += 1  # good sentence structure
        elif avg_sentence_length > 50:
            score -= 1  # too long sentences
        
        if has_transitions:
            score += 1  # good organization
        
        # Check for hesitation indicators
        hesitation_words = ['um', 'uh', 'like', 'you know', 'kind of', 'sort of']
        hesitation_count = sum(response.lower().count(word) for word in hesitation_words)
        
        if hesitation_count > 5:
            score -= 1
        
        return max(1, min(5, score))
    
    def _score_accuracy(self, response: str, question: Dict[str, Any], metadata: Dict[str, Any]) -> int:
        """
        Score technical accuracy (1-5).
        Evaluates: correctness, depth, proper terminology.
        """
        if not response or len(response.strip()) == 0:
            return 1
        
        response_lower = response.lower()
        
        # Check key points coverage
        key_points = question.get('key_points', [])
        covered_points = sum(1 for point in key_points 
                           if point.lower() in response_lower)
        
        # Scoring based on key points
        if not key_points:
            score = 3
        else:
            coverage_ratio = covered_points / len(key_points)
            if coverage_ratio < 0.3:
                score = 2
            elif coverage_ratio < 0.6:
                score = 3
            elif coverage_ratio < 0.9:
                score = 4
            else:
                score = 5
        
        # Check for depth indicators
        technical_terms = ['algorithm', 'architecture', 'pattern', 'optimization', 'trade-off', 'complexity']
        has_depth = sum(response_lower.count(term) for term in technical_terms)
        
        if has_depth >= 3:
            score = min(5, score + 1)
        
        # Check for incorrect statements (negative scoring)
        incorrect_patterns = ['never use', 'always avoid', 'should never']
        has_absolutes = any(pattern in response_lower for pattern in incorrect_patterns)
        
        if has_absolutes and covered_points < len(key_points):
            score = max(1, score - 1)
        
        return max(1, min(5, int(score)))
    
    def _score_completeness(self, response: str, question: Dict[str, Any], metadata: Dict[str, Any]) -> int:
        """
        Score completeness (1-5).
        Evaluates: all aspects covered, examples provided, edge cases considered.
        """
        if not response or len(response.strip()) == 0:
            return 1
        
        response_lower = response.lower()
        
        # Base score on response length
        length = len(response.split())
        if length < 30:
            score = 2
        elif length < 100:
            score = 3
        elif length < 200:
            score = 4
        else:
            score = 5
        
        # Bonus for examples
        example_indicators = ['for example', 'e.g.', 'for instance', 'such as', 'like when']
        has_examples = any(indicator in response_lower for indicator in example_indicators)
        
        if has_examples:
            score = min(5, score + 1)
        
        # Bonus for edge case consideration
        edge_case_indicators = ['edge case', 'corner case', 'boundary', 'special case', 'exception']
        considers_edges = any(indicator in response_lower for indicator in edge_case_indicators)
        
        if considers_edges:
            score = min(5, score + 1)
        
        # Check key points coverage as completeness indicator
        key_points = question.get('key_points', [])
        if key_points:
            covered = sum(1 for point in key_points if point.lower() in response_lower)
            if covered < len(key_points) * 0.5:
                score = max(1, score - 1)
        
        return max(1, min(5, int(score)))
    
    def _score_confidence(self, response: str, metadata: Dict[str, Any]) -> int:
        """
        Score confidence (1-5).
        Heuristic based on: hesitation indicators, tone, consistency, length.
        """
        if not response or len(response.strip()) == 0:
            return 1
        
        response_lower = response.lower()
        
        # Hesitation indicators
        hesitations = ['um', 'uh', 'like', 'you know', 'kind of', 'sort of', 'maybe', 'i think', 'i guess']
        hesitation_count = sum(response_lower.count(h) for h in hesitations)
        
        # Uncertainty indicators
        uncertainties = ["i'm not sure", "not certain", "unclear", "unclear to me", "confused"]
        uncertainty_count = sum(response_lower.count(u) for u in uncertainties)
        
        # Confidence indicators
        confident_patterns = ['definitely', 'absolutely', 'clearly', 'obviously', 'definitely', 'certain']
        confidence_count = sum(response_lower.count(p) for p in confident_patterns)
        
        # Base score on length and structure
        length = len(response.split())
        if length > 50:
            score = 3
        else:
            score = 2
        
        # Adjust based on hesitations/uncertainties
        negative_count = hesitation_count + (uncertainty_count * 2)
        
        if negative_count == 0:
            score = 4
        elif negative_count == 1:
            score = 3
        elif negative_count > 3:
            score = 1
        
        # Boost for confidence indicators
        if confidence_count >= 2:
            score = min(5, score + 1)
        
        # Check for repeated/filler words (sign of uncertainty)
        words = response_lower.split()
        if len(words) > 5:
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio < 0.6:  # too many repeated words
                score = max(1, score - 1)
        
        return max(1, min(5, int(score)))
    
    def _generate_insights(self, 
                          response: str,
                          question: Dict[str, Any],
                          scores: Dict[str, int],
                          metadata: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate strengths and gaps based on scores."""
        strengths = []
        gaps = []
        
        # Analyze strengths
        if scores['clarity'] >= 4:
            strengths.append("Well-organized and clear explanation")
        if scores['accuracy'] >= 4:
            strengths.append("Strong technical knowledge")
        if scores['completeness'] >= 4:
            strengths.append("Comprehensive answer with examples")
        if scores['confidence'] >= 4:
            strengths.append("Confident and decisive response")
        
        # Analyze gaps
        if scores['clarity'] < 3:
            gaps.append("Could improve organization and clarity")
        if scores['accuracy'] < 3:
            gaps.append("Consider deeper technical understanding")
        if scores['completeness'] < 3:
            gaps.append("Address more aspects and provide examples")
        if scores['confidence'] < 3:
            gaps.append("Speak with more confidence and certainty")
        
        # Add follow-up specific insights
        key_points = question.get('key_points', [])
        response_lower = response.lower()
        missing_points = [p for p in key_points if p.lower() not in response_lower]
        
        if missing_points:
            gaps.append(f"Missing discussion of: {', '.join(missing_points)}")
        
        return {
            'strengths': strengths if strengths else ["Adequate response"],
            'gaps': gaps if gaps else ["No significant gaps"]
        }
