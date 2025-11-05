"""
Puzzle Generator Module
Generates math problems based on difficulty level
"""
import random

class PuzzleGenerator:
    def __init__(self):
        self.difficulty_levels = {
            'easy': {'range': (1, 10), 'operations': ['+', '-']},
            'medium': {'range': (5, 50), 'operations': ['+', '-', '*']},
            'hard': {'range': (10, 100), 'operations': ['+', '-', '*', '/']}
        }
    
    def generate_puzzle(self, difficulty='easy'):
        """
        Generate a math puzzle based on difficulty level
        
        Args:
            difficulty (str): 'easy', 'medium', or 'hard'
            
        Returns:
            tuple: (question_string, correct_answer)
        """
        level = self.difficulty_levels.get(difficulty.lower(), self.difficulty_levels['easy'])
        min_val, max_val = level['range']
        operation = random.choice(level['operations'])
        
        num1 = random.randint(min_val, max_val)
        num2 = random.randint(min_val, max_val)
        
        # Create puzzle based on operation
        if operation == '+':
            answer = num1 + num2
            question = f"{num1} + {num2}"
            
        elif operation == '-':
            # Ensure positive result for easy level
            if difficulty.lower() == 'easy' and num1 < num2:
                num1, num2 = num2, num1
            answer = num1 - num2
            question = f"{num1} - {num2}"
            
        elif operation == '*':
            # Keep numbers smaller for multiplication
            num1 = random.randint(2, 12)
            num2 = random.randint(2, 12)
            answer = num1 * num2
            question = f"{num1} × {num2}"
            
        elif operation == '/':
            # Ensure clean division
            num2 = random.randint(2, 10)
            answer = random.randint(2, 10)
            num1 = num2 * answer
            question = f"{num1} ÷ {num2}"
        
        return question, answer
    
    def get_difficulty_levels(self):
        """Return list of available difficulty levels"""
        return list(self.difficulty_levels.keys())