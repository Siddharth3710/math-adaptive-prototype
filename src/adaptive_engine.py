"""
Enhanced Adaptive Engine Module
Implements advanced rule-based logic with streak detection, confidence scoring,
and dynamic adjustment windows
"""

class AdaptiveEngine:
    def __init__(self):
        self.difficulty_order = ['easy', 'medium', 'hard']
        
        # Dynamic performance window based on difficulty
        self.base_window = 3
        self.min_window = 2
        self.max_window = 5
        
        # Enhanced thresholds
        self.thresholds = {
            'accuracy_excellent': 0.9,  # 90%+ = excellent
            'accuracy_high': 0.8,       # 80%+ = increase difficulty
            'accuracy_medium': 0.6,     # 60-80% = maintain
            'accuracy_low': 0.5,        # 50% or lower = decrease
            'time_fast': 5,             # < 5s = very fast
            'time_optimal': 10,         # 5-10s = optimal
            'time_slow': 15,            # > 15s = slow
            'streak_threshold': 3,      # 3+ correct = hot streak
            'consistency_threshold': 0.8 # For confidence calculation
        }
        
        # Track adaptation history
        self.adaptation_history = []
        
    def calculate_confidence_score(self, performance_metrics, recent_attempts):
        """
        Calculate confidence score based on accuracy and consistency
        
        Args:
            performance_metrics (dict): Overall performance data
            recent_attempts (list): List of recent attempt results (True/False)
        
        Returns:
            float: Confidence score (0-1)
        """
        if not recent_attempts:
            return 0.5  # Neutral confidence
        
        accuracy = performance_metrics['accuracy']
        
        # Calculate consistency (how stable is performance)
        # Lower variance in times = higher consistency
        times = performance_metrics.get('times', [])
        if len(times) > 1:
            avg_time = sum(times) / len(times)
            variance = sum((t - avg_time) ** 2 for t in times) / len(times)
            time_consistency = max(0, 1 - (variance / 100))  # Normalize
        else:
            time_consistency = 0.5
        
        # Calculate pattern consistency (alternating vs steady performance)
        if len(recent_attempts) >= 3:
            # Check for alternating pattern (bad sign)
            alternating = sum(1 for i in range(len(recent_attempts)-1) 
                            if recent_attempts[i] != recent_attempts[i+1])
            pattern_consistency = 1 - (alternating / len(recent_attempts))
        else:
            pattern_consistency = 0.5
        
        # Weighted confidence score
        confidence = (
            accuracy * 0.5 +                    # 50% weight on accuracy
            time_consistency * 0.25 +           # 25% weight on time consistency
            pattern_consistency * 0.25          # 25% weight on pattern
        )
        
        return min(1.0, max(0.0, confidence))
    
    def detect_streak(self, recent_attempts):
        """
        Detect hot/cold streaks in performance
        
        Args:
            recent_attempts (list): List of recent attempt results (True/False)
        
        Returns:
            dict: Streak information
        """
        if not recent_attempts:
            return {'type': 'none', 'length': 0}
        
        # Count current streak from the end
        current_result = recent_attempts[-1]
        streak_length = 1
        
        for i in range(len(recent_attempts) - 2, -1, -1):
            if recent_attempts[i] == current_result:
                streak_length += 1
            else:
                break
        
        streak_type = 'hot' if current_result else 'cold'
        
        return {
            'type': streak_type,
            'length': streak_length,
            'is_significant': streak_length >= self.thresholds['streak_threshold']
        }
    
    def get_dynamic_window(self, current_difficulty, confidence_score):
        """
        Calculate dynamic adjustment window based on difficulty and confidence
        
        Args:
            current_difficulty (str): Current difficulty level
            confidence_score (float): Confidence score (0-1)
        
        Returns:
            int: Number of attempts to consider
        """
        # Higher difficulty = larger window (more data needed)
        difficulty_factor = self.difficulty_order.index(current_difficulty.lower())
        
        # Lower confidence = larger window (need more evidence)
        confidence_factor = 1 - confidence_score
        
        # Calculate window size
        window = self.base_window + difficulty_factor + int(confidence_factor * 2)
        
        return max(self.min_window, min(window, self.max_window))
    
    def decide_next_difficulty(self, current_difficulty, performance_metrics, 
                               recent_attempts_list, attempts_since_last_adjustment):
        """
        Enhanced decision logic with streak detection and confidence scoring
        
        Args:
            current_difficulty (str): Current difficulty level
            performance_metrics (dict): Recent performance data
            recent_attempts_list (list): List of recent correctness (True/False)
            attempts_since_last_adjustment (int): Questions since last change
        
        Returns:
            tuple: (next_difficulty, decision_details)
        """
        
        # Need minimum attempts to adapt
        if performance_metrics['total_attempts'] < 2:
            return current_difficulty, {'reason': 'insufficient_data', 'confidence': 0}
        
        # Calculate confidence score
        confidence = self.calculate_confidence_score(performance_metrics, recent_attempts_list)
        
        # Detect streaks
        streak_info = self.detect_streak(recent_attempts_list)
        
        # Get dynamic window
        optimal_window = self.get_dynamic_window(current_difficulty, confidence)
        
        # Extract metrics
        accuracy = performance_metrics['accuracy']
        avg_time = performance_metrics['avg_time']
        
        current_index = self.difficulty_order.index(current_difficulty.lower())
        
        # Enhanced scoring system
        adjustment_score = 0
        decision_factors = []
        
        # Factor 1: Accuracy (most important) - weighted by confidence
        if accuracy >= self.thresholds['accuracy_excellent']:
            adjustment_score += 3 * confidence
            decision_factors.append(f"Excellent accuracy ({accuracy*100:.0f}%)")
        elif accuracy >= self.thresholds['accuracy_high']:
            adjustment_score += 2 * confidence
            decision_factors.append(f"High accuracy ({accuracy*100:.0f}%)")
        elif accuracy <= self.thresholds['accuracy_low']:
            adjustment_score -= 2 * confidence
            decision_factors.append(f"Low accuracy ({accuracy*100:.0f}%)")
        elif accuracy >= self.thresholds['accuracy_medium']:
            decision_factors.append(f"Steady accuracy ({accuracy*100:.0f}%)")
        
        # Factor 2: Streak detection (powerful signal)
        if streak_info['is_significant']:
            if streak_info['type'] == 'hot':
                streak_bonus = min(2, streak_info['length'] / 3)
                adjustment_score += streak_bonus
                decision_factors.append(f"Hot streak ({streak_info['length']} correct)")
            else:
                streak_penalty = min(2, streak_info['length'] / 3)
                adjustment_score -= streak_penalty
                decision_factors.append(f"Cold streak ({streak_info['length']} incorrect)")
        
        # Factor 3: Speed (secondary factor, only if doing reasonably well)
        if accuracy >= self.thresholds['accuracy_medium']:
            if avg_time < self.thresholds['time_fast']:
                adjustment_score += 1
                decision_factors.append(f"Fast responses ({avg_time:.1f}s avg)")
            elif avg_time > self.thresholds['time_slow']:
                adjustment_score -= 0.5
                decision_factors.append(f"Slow responses ({avg_time:.1f}s avg)")
        
        # Factor 4: Confidence modifier
        # High confidence = more willing to adjust
        # Low confidence = more conservative
        if confidence < 0.4:
            adjustment_score *= 0.5  # Reduce adjustment if uncertain
            decision_factors.append("Low confidence - being conservative")
        elif confidence > 0.8:
            adjustment_score *= 1.2  # Increase adjustment if confident
            decision_factors.append("High confidence in assessment")
        
        # Make decision based on score
        new_index = current_index
        adjustment_type = 'maintain'
        
        # Thresholds adjusted by confidence
        increase_threshold = 2.0 * (1 - confidence * 0.2)  # Lower if confident
        decrease_threshold = -2.0 * (1 - confidence * 0.2)
        
        if adjustment_score >= increase_threshold and attempts_since_last_adjustment >= optimal_window:
            # Increase difficulty
            new_index = min(current_index + 1, len(self.difficulty_order) - 1)
            adjustment_type = 'increase'
        elif adjustment_score <= decrease_threshold and attempts_since_last_adjustment >= optimal_window:
            # Decrease difficulty
            new_index = max(current_index - 1, 0)
            adjustment_type = 'decrease'
        
        next_difficulty = self.difficulty_order[new_index]
        
        # Record adaptation decision
        decision_details = {
            'old_difficulty': current_difficulty,
            'new_difficulty': next_difficulty,
            'adjustment_score': adjustment_score,
            'confidence': confidence,
            'streak': streak_info,
            'factors': decision_factors,
            'type': adjustment_type,
            'optimal_window': optimal_window,
            'attempts_evaluated': attempts_since_last_adjustment
        }
        
        self.adaptation_history.append(decision_details)
        
        return next_difficulty, decision_details
    
    def get_detailed_recommendation(self, decision_details, metrics):
        """
        Generate detailed explanation for difficulty change
        
        Returns:
            str: Comprehensive human-readable explanation
        """
        old_diff = decision_details['old_difficulty']
        new_diff = decision_details['new_difficulty']
        confidence = decision_details['confidence']
        streak = decision_details['streak']
        
        if old_diff == new_diff:
            base_msg = "Maintaining current difficulty - "
            
            if confidence > 0.7:
                return base_msg + "steady, confident performance"
            elif metrics['accuracy'] >= 0.6:
                return base_msg + "good progress, building mastery"
            else:
                return base_msg + "need more data to assess"
        
        # Build explanation for change
        explanation_parts = []
        
        # Main reason
        accuracy_pct = metrics['accuracy'] * 100
        if new_diff == 'hard' and old_diff == 'medium':
            explanation_parts.append(f"🌟 Outstanding! {accuracy_pct:.0f}% accuracy - moving to HARD")
        elif new_diff == 'medium' and old_diff == 'easy':
            explanation_parts.append(f"🎯 Great progress! {accuracy_pct:.0f}% accuracy - advancing to MEDIUM")
        elif new_diff == 'easy' and old_diff == 'medium':
            explanation_parts.append(f"📚 Adjusting to EASY for better learning pace")
        elif new_diff == 'medium' and old_diff == 'hard':
            explanation_parts.append(f"⚖️ Adjusting to MEDIUM to optimize learning")
        
        # Add streak info if significant
        if streak['is_significant']:
            if streak['type'] == 'hot':
                explanation_parts.append(f"(🔥 {streak['length']}-question hot streak!)")
            else:
                explanation_parts.append(f"(Let's build momentum with adjusted difficulty)")
        
        # Add confidence indicator
        if confidence > 0.8:
            explanation_parts.append(f"[High confidence: {confidence:.0%}]")
        
        return " ".join(explanation_parts)
    
    def get_encouragement(self, metrics, streak_info):
        """
        Generate encouraging feedback with streak awareness
        
        Returns:
            str: Encouraging message
        """
        accuracy = metrics['accuracy'] * 100
        
        # Streak-based encouragement
        if streak_info['is_significant']:
            if streak_info['type'] == 'hot':
                return f"🔥 ON FIRE! {streak_info['length']} correct in a row! Keep it up!"
            else:
                return "💪 Don't worry! Every expert was once a beginner. Let's try again!"
        
        # Standard encouragement
        if accuracy >= 90:
            return "⭐ Outstanding work! You're a math superstar!"
        elif accuracy >= 75:
            return "👍 Great job! Keep up the excellent work!"
        elif accuracy >= 60:
            return "💪 Good effort! You're making solid progress!"
        else:
            return "🎯 Keep practicing! Every mistake teaches us something new!"
    
    def get_adaptation_summary(self):
        """
        Get summary of all adaptations during session
        
        Returns:
            dict: Adaptation statistics
        """
        if not self.adaptation_history:
            return None
        
        total_adaptations = len(self.adaptation_history)
        increases = sum(1 for d in self.adaptation_history if d['type'] == 'increase')
        decreases = sum(1 for d in self.adaptation_history if d['type'] == 'decrease')
        maintains = total_adaptations - increases - decreases
        
        avg_confidence = sum(d['confidence'] for d in self.adaptation_history) / total_adaptations
        
        return {
            'total_evaluations': total_adaptations,
            'difficulty_increases': increases,
            'difficulty_decreases': decreases,
            'maintained': maintains,
            'average_confidence': avg_confidence
        }