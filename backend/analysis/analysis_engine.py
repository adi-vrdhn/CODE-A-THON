from typing import Dict, List, Any
from statistics import mean, stdev

class AnalysisEngine:
    """Analyzes interview results and generates insights."""
    
    def analyze_interview(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze all interview results.
        
        Args:
            results: List of individual question results with scores
        
        Returns:
            Complete analysis with patterns, recommendations, and aggregated metrics
        """
        if not results:
            return self._empty_analysis()
        
        return {
            'aggregate_scores': self._calculate_aggregate_scores(results),
            'dimension_analysis': self._analyze_dimensions(results),
            'patterns': self._identify_patterns(results),
            'consistency': self._analyze_consistency(results),
            'recommendations': self._generate_recommendations(results),
            'summary': self._generate_summary(results)
        }
    
    def _calculate_aggregate_scores(self, results: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate aggregated scores across all questions."""
        dimensions = ['clarity', 'accuracy', 'completeness', 'confidence']
        
        aggregates = {}
        for dimension in dimensions:
            scores = [r['scores'][dimension] for r in results if dimension in r['scores']]
            if scores:
                aggregates[dimension] = round(mean(scores), 2)
        
        # Overall score
        overall_scores = [r['overall'] for r in results]
        aggregates['overall'] = round(mean(overall_scores), 2) if overall_scores else 0
        
        return aggregates
    
    def _analyze_dimensions(self, results: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Analyze performance by dimension."""
        dimensions = ['clarity', 'accuracy', 'completeness', 'confidence']
        analysis = {}
        
        for dimension in dimensions:
            scores = [r['scores'][dimension] for r in results if dimension in r['scores']]
            
            if not scores:
                continue
            
            avg = mean(scores)
            min_score = min(scores)
            max_score = max(scores)
            std_dev = stdev(scores) if len(scores) > 1 else 0
            
            analysis[dimension] = {
                'average': round(avg, 2),
                'min': min_score,
                'max': max_score,
                'consistency': round(5 - std_dev, 2),  # lower stddev = higher consistency
                'trend': self._calculate_trend(scores)
            }
        
        return analysis
    
    def _calculate_trend(self, scores: List[int]) -> str:
        """Calculate if performance is improving, declining, or stable."""
        if len(scores) < 2:
            return "stable"
        
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        first_avg = mean(first_half)
        second_avg = mean(second_half)
        
        diff = second_avg - first_avg
        
        if diff > 0.5:
            return "improving"
        elif diff < -0.5:
            return "declining"
        else:
            return "stable"
    
    def _identify_patterns(self, results: List[Dict[str, Any]]) -> List[str]:
        """Identify patterns in performance."""
        patterns = []
        
        # Aggregate metrics
        agg = self._calculate_aggregate_scores(results)
        
        # Find strongest dimension
        dimensions = ['clarity', 'accuracy', 'completeness', 'confidence']
        dimension_scores = {d: agg[d] for d in dimensions}
        strongest = max(dimension_scores, key=dimension_scores.get)
        weakest = min(dimension_scores, key=dimension_scores.get)
        
        patterns.append(f"Strongest dimension: {strongest.capitalize()} ({dimension_scores[strongest]}/5)")
        patterns.append(f"Needs improvement: {weakest.capitalize()} ({dimension_scores[weakest]}/5)")
        
        # Consistency pattern
        overall_scores = [r['overall'] for r in results]
        if len(overall_scores) > 1:
            std_dev = stdev(overall_scores)
            if std_dev < 0.5:
                patterns.append("Very consistent performance across all questions")
            elif std_dev > 1.0:
                patterns.append("Performance varies significantly across questions")
        
        # Score distribution pattern
        high_scores = sum(1 for r in results if r['overall'] >= 4)
        low_scores = sum(1 for r in results if r['overall'] < 3)
        
        if high_scores > len(results) * 0.6:
            patterns.append("Consistently strong performance")
        elif low_scores > len(results) * 0.6:
            patterns.append("Needs significant improvement")
        else:
            patterns.append("Mixed performance with both strengths and areas for growth")
        
        # Technical accuracy vs soft skills
        tech_dims = ['accuracy']
        soft_dims = ['clarity', 'confidence']
        
        tech_avg = mean([agg[d] for d in tech_dims])
        soft_avg = mean([agg[d] for d in soft_dims])
        
        if tech_avg > soft_avg + 1:
            patterns.append("Stronger in technical knowledge than communication")
        elif soft_avg > tech_avg + 1:
            patterns.append("Better at communication than technical depth")
        
        return patterns
    
    def _analyze_consistency(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze consistency of performance."""
        overall_scores = [r['overall'] for r in results]
        
        if len(overall_scores) < 2:
            return {
                'score': 0,
                'interpretation': "Insufficient data for consistency analysis"
            }
        
        std_dev = stdev(overall_scores)
        # Normalize to 1-5 scale
        consistency_score = max(1, min(5, 5 - std_dev))
        
        interpretation = ""
        if consistency_score >= 4:
            interpretation = "Very consistent performance"
        elif consistency_score >= 3:
            interpretation = "Moderately consistent performance"
        else:
            interpretation = "Inconsistent performance"
        
        return {
            'score': round(consistency_score, 2),
            'std_dev': round(std_dev, 2),
            'interpretation': interpretation
        }
    
    def _generate_recommendations(self, results: List[Dict[str, Any]]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        agg = self._calculate_aggregate_scores(results)
        
        # Recommendations based on low scores
        if agg['clarity'] < 3:
            recommendations.append("Practice structuring your thoughts more clearly before answering")
            recommendations.append("Work on explaining complex concepts in simpler terms")
        
        if agg['accuracy'] < 3:
            recommendations.append("Deepen your technical knowledge in core concepts")
            recommendations.append("Study key terminology and use it correctly in responses")
        
        if agg['completeness'] < 3:
            recommendations.append("Provide more concrete examples when answering")
            recommendations.append("Consider edge cases and alternative scenarios")
        
        if agg['confidence'] < 3:
            recommendations.append("Build confidence through practice and preparation")
            recommendations.append("Work on eliminating filler words and hesitations")
        
        # Overall recommendations
        if agg['overall'] >= 4:
            recommendations.append("Excellent overall performance - maintain this level")
        elif agg['overall'] >= 3:
            recommendations.append("Good foundation - focus on weak areas to improve further")
        else:
            recommendations.append("Significant improvement needed - prioritize technical skill building")
        
        # Role-specific recommendations
        if agg['clarity'] > agg['accuracy']:
            recommendations.append("While you're clear, deepen your technical expertise")
        else:
            recommendations.append("Improve communication to better convey your technical knowledge")
        
        return recommendations if recommendations else ["Continue practicing interview techniques"]
    
    def _generate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate executive summary."""
        agg = self._calculate_aggregate_scores(results)
        overall = agg['overall']
        
        if overall >= 4.5:
            level = "Exceptional"
        elif overall >= 4:
            level = "Strong"
        elif overall >= 3:
            level = "Proficient"
        elif overall >= 2:
            level = "Developing"
        else:
            level = "Needs Improvement"
        
        return {
            'overall_level': level,
            'score': overall,
            'questions_answered': len(results),
            'interpretation': f"Candidate demonstrates {level.lower()} interview performance"
        }
    
    def _empty_analysis(self) -> Dict[str, Any]:
        """Return empty analysis structure."""
        return {
            'aggregate_scores': {},
            'dimension_analysis': {},
            'patterns': [],
            'consistency': {},
            'recommendations': ["Complete the interview to receive analysis"],
            'summary': {}
        }
