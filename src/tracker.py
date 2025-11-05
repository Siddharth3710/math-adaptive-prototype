"""
Performance Tracker Module
Tracks user performance metrics across the session
"""

import time
import os
import json
from datetime import datetime


class PerformanceTracker:
    def __init__(self, username):
        self.username = username
        self.session_start = datetime.now()
        self.attempts = []
        self.current_difficulty = None

    def record_attempt(self, question, user_answer, correct_answer,
                       time_taken, difficulty):
        """
        Record a single attempt

        Args:
            question (str): The math question asked
            user_answer: User's answer
            correct_answer: Correct answer
            time_taken (float): Time in seconds
            difficulty (str): Current difficulty level
        """
        is_correct = (user_answer == correct_answer)

        attempt = {
            'question': question,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
            'time_taken': time_taken,
            'difficulty': difficulty,
            'timestamp': datetime.now()
        }

        self.attempts.append(attempt)
        self.current_difficulty = difficulty

        return is_correct

    def get_recent_performance(self, n=3):
        """
        Get performance metrics for last n attempts

        Returns:
            dict: Performance metrics
        """
        if not self.attempts:
            return {
                'accuracy': 0,
                'avg_time': 0,
                'total_attempts': 0,
                'attempts_list': [],
                'times': []
            }

        recent = self.attempts[-n:] if len(self.attempts) >= n else self.attempts

        correct_count = sum(1 for a in recent if a['is_correct'])
        total_count = len(recent)
        avg_time = sum(a['time_taken'] for a in recent) / total_count

        return {
            'accuracy': correct_count / total_count if total_count > 0 else 0,
            'avg_time': avg_time,
            'total_attempts': total_count,
            'correct_count': correct_count,
            'attempts_list': [a['is_correct'] for a in recent],
            'times': [a['time_taken'] for a in recent]
        }

    def get_session_summary(self):
        """
        Generate end-of-session summary

        Returns:
            dict: Complete session statistics
        """
        if not self.attempts:
            return None

        total = len(self.attempts)
        correct = sum(1 for a in self.attempts if a['is_correct'])
        accuracy = (correct / total * 100) if total > 0 else 0
        avg_time = sum(a['time_taken'] for a in self.attempts) / total

        # Difficulty progression
        difficulty_changes = [a['difficulty'] for a in self.attempts]

        # Operation breakdown
        operation_breakdown = self.get_operation_breakdown()

        # Learning velocity (simple trend)
        learning_velocity = self.get_learning_velocity()

        return {
            'username': self.username,
            'total_questions': total,
            'correct_answers': correct,
            'accuracy_percentage': accuracy,
            'average_time': avg_time,
            'final_difficulty': self.current_difficulty,
            'difficulty_progression': difficulty_changes,
            'session_duration': (datetime.now() - self.session_start).seconds,
            'operation_breakdown': operation_breakdown,
            'learning_velocity': learning_velocity
        }

    def get_operation_breakdown(self):
        """Return breakdown of performance by operation type"""
        breakdown = {}
        for a in self.attempts:
            if '+' in a['question']:
                op = 'addition'
            elif '-' in a['question']:
                op = 'subtraction'
            elif '×' in a['question']:
                op = 'multiplication'
            elif '÷' in a['question']:
                op = 'division'
            else:
                op = 'other'

            if op not in breakdown:
                breakdown[op] = {'total': 0, 'correct': 0}
            breakdown[op]['total'] += 1
            if a['is_correct']:
                breakdown[op]['correct'] += 1

        for op, stats in breakdown.items():
            stats['accuracy'] = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
        return breakdown

    def get_learning_velocity(self):
        """Estimate improvement trend across session"""
        if len(self.attempts) < 4:
            return {'trend': 'insufficient_data'}

        midpoint = len(self.attempts) // 2
        first_half = self.attempts[:midpoint]
        second_half = self.attempts[midpoint:]

        acc1 = sum(1 for a in first_half if a['is_correct']) / len(first_half)
        acc2 = sum(1 for a in second_half if a['is_correct']) / len(second_half)

        if acc2 > acc1 + 0.1:
            trend = 'improving'
        elif acc1 > acc2 + 0.1:
            trend = 'declining'
        else:
            trend = 'stable'

        return {'trend': trend, 'start_accuracy': acc1, 'end_accuracy': acc2}

    def display_summary(self):
        """Print formatted session summary"""
        summary = self.get_session_summary()

        if not summary:
            print("No attempts recorded yet.")
            return

        print("\n" + "=" * 50)
        print(f"SESSION SUMMARY FOR {summary['username'].upper()}")
        print("=" * 50)
        print(f"Total Questions: {summary['total_questions']}")
        print(f"Correct Answers: {summary['correct_answers']}")
        print(f"Accuracy: {summary['accuracy_percentage']:.1f}%")
        print(f"Average Time per Question: {summary['average_time']:.1f} seconds")
        print(f"Final Difficulty Level: {summary['final_difficulty'].upper()}")
        print(f"Session Duration: {summary['session_duration']} seconds")
        print("\nDifficulty Progression:")
        print(" → ".join(summary['difficulty_progression']))
        print("=" * 50)
    def display_progress_indicator(self, question_count, questions_until_check):
        """Display a simple progress indicator in the console"""
        print(f"\n📈 Progress: Question {question_count}")
        if questions_until_check > 0:
            print(f"   🔄 System will re-evaluate difficulty after {questions_until_check} more question(s).")
        else:
            print("   ⚙️ Evaluating your recent performance for difficulty adjustment...")


    # ────────────────────────────────
    # SESSION PERSISTENCE METHODS
    # ────────────────────────────────

    @staticmethod
    def list_user_sessions(username):
        """List saved session files for the given user in data/sessions"""
        session_dir = os.path.join("data", "sessions")
        if not os.path.exists(session_dir):
            return []
        files = [
            os.path.join(session_dir, f)
            for f in os.listdir(session_dir)
            if f.startswith(f"{username}_") and f.endswith(".json")
        ]
        return sorted(files, key=os.path.getmtime, reverse=True)

    def save_session(self):
        """Save current session data to JSON file in data/sessions"""
        session_dir = os.path.join("data", "sessions")
        os.makedirs(session_dir, exist_ok=True)

        data = self.get_session_summary()
        timestamp = int(time.time())
        filename = f"{self.username}_{timestamp}.json"
        filepath = os.path.join(session_dir, filename)

        with open(filepath, "w") as f:
            json.dump(data, f, default=str, indent=2)

        print(f"💾 Session saved successfully at {filepath}")
        return filepath

    @staticmethod
    def load_session(filepath):
        """Load session data from JSON file"""
        with open(filepath, "r") as f:
            return json.load(f)
