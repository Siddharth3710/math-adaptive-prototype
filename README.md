# 🎓 Math Adventures - Adaptive Learning System

An AI-powered adaptive math learning prototype that adjusts puzzle difficulty based on student performance in real-time.

## 📋 Overview

This project implements an adaptive learning system designed for children ages 5-10 to practice basic math operations (addition, subtraction, multiplication, and division). The system uses rule-based logic to dynamically adjust difficulty levels, keeping learners in their optimal challenge zone.

## 🎯 Key Features

- **Dynamic Difficulty Adjustment**: Automatically adapts to student performance
- **Three Difficulty Levels**: Easy, Medium, and Hard
- **Performance Tracking**: Monitors correctness and response time
- **Real-time Feedback**: Immediate feedback after each question
- **Session Summary**: Comprehensive end-of-session statistics
- **Encouragement System**: Motivational messages based on performance

## 🏗️ Architecture

### Components

1. **Puzzle Generator** (`puzzle_generator.py`)
   - Creates math problems dynamically based on difficulty level
   - Supports addition, subtraction, multiplication, and division
   - Ensures age-appropriate number ranges

2. **Performance Tracker** (`tracker.py`)
   - Logs user attempts, correctness, and time taken
   - Calculates accuracy and average response time
   - Generates session summaries

3. **Adaptive Engine** (`adaptive_engine.py`)
   - Implements rule-based logic for difficulty adjustment
   - Analyzes recent performance (last 3 attempts)
   - Makes decisions based on accuracy and speed

4. **Main Application** (`main.py`)
   - Orchestrates the learning flow
   - Handles user interaction
   - Integrates all components

### System Flow

```
Start → User Input (Name + Initial Difficulty) → Generate Puzzle → 
User Answers → Track Performance → Adaptive Logic (every 3 questions) → 
Adjust Difficulty → Next Puzzle → ... → Session Summary
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- No external libraries required (uses Python standard library only)

### Installation

1. Clone the repository:
```bash
git https://github.com/Siddharth3710/math-adaptive-prototype.git

cd math-adaptive-prototype
```

2. Run the application:
```bash
python src/main.py
```

## 📖 Usage

1. Enter your name when prompted
2. Choose initial difficulty level (1=Easy, 2=Medium, 3=Hard)
3. Answer math questions as they appear
4. The system will automatically adjust difficulty based on your performance
5. Type 'quit' anytime to end the session and view your summary

### Example Session

```
🎓 MATH ADVENTURES - Adaptive Learning System
Welcome! This system adapts to YOUR learning pace.

Enter your name: Alex

Hi Alex! Choose your starting difficulty level:
1. Easy (ages 5-7): Addition and subtraction with small numbers
2. Medium (ages 7-9): Includes multiplication
3. Hard (ages 9-10): All operations including division

Enter 1, 2, or 3: 2

Question 1 | Difficulty: MEDIUM
15 + 23 = ?
Your answer: 38
✅ Correct! (3.2 seconds)
```

## 🧠 Adaptive Logic

### Rule-Based Algorithm

The adaptive engine uses a scoring system based on two factors:

1. **Accuracy** (Primary Factor)
   - ≥80% correct → Strong signal to increase difficulty (+2 points)
   - ≤50% correct → Strong signal to decrease difficulty (-2 points)

2. **Response Time** (Secondary Factor)
   - Fast (<5s) + High accuracy → Increase difficulty (+1 point)
   - Slow (>15s) → May decrease difficulty (-1 point)

### Decision Thresholds

- **Increase Difficulty**: Score ≥ 2 (consistently correct + fast)
- **Decrease Difficulty**: Score ≤ -2 (struggling or slow)
- **Maintain Level**: -1 < Score < 2 (steady performance)

### Why Rule-Based?

- **Interpretability**: Easy to explain and understand
- **No Training Data Required**: Works immediately without data collection
- **Predictable Behavior**: Consistent and reliable adjustments
- **Low Latency**: Instant decisions without model inference

## 📊 Metrics Tracked

- **Correctness**: Binary (correct/incorrect)
- **Response Time**: Seconds per question
- **Accuracy Rate**: Percentage correct over last 3 attempts
- **Difficulty Progression**: Track of difficulty level changes
- **Session Duration**: Total time spent

## 🎓 Educational Design Principles

1. **Zone of Proximal Development**: Keeps difficulty at optimal challenge level
2. **Immediate Feedback**: Reinforces learning after each attempt
3. **Mastery-Based Progression**: Only advances when ready
4. **Positive Reinforcement**: Encouraging messages maintain motivation

## 🔮 Future Enhancements

### Potential ML Approach

Could implement:
- **Logistic Regression**: Predict probability of correct answer
- **Decision Trees**: Learn complex performance patterns
- **Reinforcement Learning**: Optimize difficulty for maximum learning

### Data Collection for ML

To train a model, collect:
- Student demographics (age, grade level)
- Problem characteristics (operation, numbers used)
- Temporal patterns (time of day, fatigue indicators)
- Learning outcomes over multiple sessions

### Scaling to Other Topics

The architecture can extend to:
- **Language Arts**: Vocabulary, spelling, grammar
- **Science**: Concept questions, experiments
- **Reading Comprehension**: Passage difficulty adjustment

## 🤔 Trade-offs: Rule-Based vs ML

| Aspect | Rule-Based | ML-Based |
|--------|-----------|----------|
| **Setup** | Immediate | Requires training data |
| **Interpretability** | Clear logic | Black box |
| **Adaptability** | Manual tuning | Learns from data |
| **Accuracy** | Good for simple patterns | Better for complex patterns |
| **Maintenance** | Easy to update | Needs retraining |

## 📁 Project Structure

```
math-adaptive-prototype/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── src/
│   ├── main.py               # Main application entry point
│   ├── puzzle_generator.py   # Math puzzle generation
│   ├── tracker.py            # Performance tracking
│   └── adaptive_engine.py    # Adaptive logic
└── data/                     # (Optional) Store session logs
```

## 🤝 Contributing

This is an educational project. Feel free to:
- Report bugs
- Suggest improvements
- Add new features
- Implement ML-based adaptive engine

## 📝 Technical Note

For the complete technical explanation including:
- Detailed architecture diagrams
- Algorithm pseudocode
- Performance metrics analysis
- Design decisions and rationale

Please refer to the accompanying technical document.

## 👤 Author

Siddharth Jha
50siddharthjha@gmail.com

## 📄 License

This project is created for educational purposes as part of an Adaptive Learning assignment.

## 🙏 Acknowledgments

- Assignment brief provided by TheProductWorks.in
- Inspired by adaptive learning research and intelligent tutoring systems