"""
Adaptive Math Learning System - Console Interface
with improved UX, progress tracking, and session persistence
"""
import time
from puzzle_generator import PuzzleGenerator
from tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine

def get_user_input(prompt, input_type=str, valid_options=None):
    """Helper function for validated input"""
    while True:
        try:
            user_input = input(prompt).strip()
            
            if input_type == int:
                user_input = int(user_input)
            
            if valid_options and user_input.lower() not in valid_options:
                print(f"Please choose from: {', '.join(valid_options)}")
                continue
            
            return user_input
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")
        except KeyboardInterrupt:
            print("\n\nSession ended by user.")
            return None

def display_welcome():
    """Display welcome screen"""
    print("\n" + "="*70)
    print("🎓 MATH ADVENTURES - Enhanced Adaptive Learning System")
    print("="*70)
    print("\n✨ Features:")
    print("  • Intelligent difficulty adaptation with confidence scoring")
    print("  • Hot/cold streak detection")
    print("  • Learning velocity tracking")
    print("  • Performance breakdown by operation type")
    print("  • Session history and persistence")
    print("\n" + "="*70 + "\n")

def check_for_previous_sessions(username, tracker_class):
    """Check if user has previous sessions and offer to view them"""
    sessions = tracker_class.list_user_sessions(username)
    
    if sessions:
        print(f"\n📚 Found {len(sessions)} previous session(s) for {username}!")
        view_choice = input("Would you like to see your previous best session? (yes/no): ").strip().lower()
        
        if view_choice in ['yes', 'y']:
            # Load and display most recent session
            latest_session = tracker_class.load_session(sessions[0])
            if latest_session:
                print(f"\n{'='*70}")
                print("📊 YOUR PREVIOUS SESSION:")
                print(f"{'='*70}")
                print(f"Questions Answered: {latest_session['total_questions']}")
                print(f"Accuracy: {latest_session['accuracy_percentage']:.1f}%")
                print(f"Final Difficulty: {latest_session['final_difficulty'].upper()}")
                
                if latest_session['learning_velocity']['trend'] == 'improving':
                    print("Trend: 📈 You were improving!")
                
                print(f"{'='*70}\n")
                input("Press Enter to start a new session...")

def main():
    """Enhanced main application flow"""
    
    display_welcome()
    
    # Initialize components
    puzzle_gen = PuzzleGenerator()
    adaptive_engine = AdaptiveEngine()
    
    # Step 1: Get user name
    username = get_user_input("👤 Enter your name: ", str)
    if username is None:
        return
    
    # Check for previous sessions
    check_for_previous_sessions(username, PerformanceTracker)
    
    tracker = PerformanceTracker(username)
    
    # Step 2: Choose initial difficulty
    print(f"\n👋 Hi {username}! Choose your starting difficulty level:")
    print("  1. Easy (ages 5-7): Addition and subtraction with small numbers")
    print("  2. Medium (ages 7-9): Includes multiplication")
    print("  3. Hard (ages 9-10): All operations including division")
    
    difficulty_choice = get_user_input("\nEnter 1, 2, or 3: ", str, ['1', '2', '3'])
    if difficulty_choice is None:
        return
    
    difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard'}
    current_difficulty = difficulty_map[difficulty_choice]
    
    print(f"\n✅ Starting at {current_difficulty.upper()} level!")
    print("\n📋 Instructions:")
    print("  • Answer each math question")
    print("  • Type 'quit' anytime to end session")
    print("  • The system adapts based on your performance")
    print("  • Try to maintain both accuracy and speed!")
    print()
    
    input("Press Enter to start your adaptive learning journey...")
    
    # Step 3: Main learning loop
    question_count = 0
    attempts_since_adjustment = 0
    last_adjustment_question = 0
    
    while True:
        question_count += 1
        attempts_since_adjustment += 1
        
        print("\n" + "─"*70)
        print(f"Question {question_count} │ Difficulty: {current_difficulty.upper()}")
        print("─"*70)
        
        # Show progress indicator
        recent_perf = tracker.get_recent_performance(3)
        if question_count > 1 and attempts_since_adjustment < 5:
            questions_until_check = max(1, 3 - attempts_since_adjustment)
            tracker.display_progress_indicator(question_count, questions_until_check)
        
        # Generate puzzle
        question, correct_answer = puzzle_gen.generate_puzzle(current_difficulty)
        
        # Ask question and time response
        print(f"\n❓ {question} = ?")
        start_time = time.time()
        
        user_answer = input("Your answer (or 'quit'): ").strip()
        
        if user_answer.lower() == 'quit':
            print("\n👋 Thanks for practicing!")
            break
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        # Validate answer
        try:
            user_answer = int(user_answer)
        except ValueError:
            print("⚠️  Please enter a number!")
            continue
        
        # Record attempt
        is_correct = tracker.record_attempt(
            question, 
            user_answer, 
            correct_answer, 
            time_taken, 
            current_difficulty
        )
        
        # Provide detailed feedback
        if is_correct:
            if time_taken < 3:
                print(f"✅ Correct! ⚡ Lightning fast! ({time_taken:.1f}s)")
            elif time_taken < 5:
                print(f"✅ Correct! 🎯 Great speed! ({time_taken:.1f}s)")
            else:
                print(f"✅ Correct! ({time_taken:.1f}s)")
        else:
            print(f"❌ Incorrect. The answer was {correct_answer}")
            if time_taken < 3:
                print("   💡 Tip: Take a moment to double-check your work!")
        
        # Show running accuracy after a few questions
        if question_count >= 3:
            recent = tracker.get_recent_performance(min(5, question_count))
            print(f"   📊 Recent accuracy: {recent['accuracy']*100:.0f}% "
                  f"(last {recent['total_attempts']} questions)")
        
        # Enhanced adaptive logic with dynamic window
        if question_count >= 2:  # Can start adapting after 2 questions
            recent_performance = tracker.get_recent_performance(
                min(question_count, 5)
            )
            
            # Get confidence-based dynamic window
            confidence = adaptive_engine.calculate_confidence_score(
                recent_performance,
                recent_performance['attempts_list']
            )
            optimal_window = adaptive_engine.get_dynamic_window(
                current_difficulty, 
                confidence
            )
            
            # Check if it's time to adjust
            should_check_adjustment = (
                attempts_since_adjustment >= optimal_window or
                (attempts_since_adjustment >= 2 and confidence > 0.8)
            )
            
            if should_check_adjustment:
                old_difficulty = current_difficulty
                
                # Get streak info for encouragement
                streak_info = adaptive_engine.detect_streak(
                    recent_performance['attempts_list']
                )
                
                # Decide next difficulty
                current_difficulty, decision_details = adaptive_engine.decide_next_difficulty(
                    current_difficulty,
                    recent_performance,
                    recent_performance['attempts_list'],
                    attempts_since_adjustment
                )
                
                # Show adaptation message
                if old_difficulty != current_difficulty:
                    print("\n" + "🔄 " + "─"*66)
                    reason = adaptive_engine.get_detailed_recommendation(
                        decision_details,
                        recent_performance
                    )
                    print(f"   {reason}")
                    
                    # Show factors considered
                    if len(decision_details['factors']) > 0:
                        print(f"   📋 Factors: {', '.join(decision_details['factors'][:2])}")
                    
                    print("─"*70)
                    attempts_since_adjustment = 0
                    last_adjustment_question = question_count
                
                # Show encouragement
                encouragement = adaptive_engine.get_encouragement(
                    recent_performance, 
                    streak_info
                )
                print(f"\n   {encouragement}")
        
        # Ask if user wants to continue after milestone
        if question_count >= 5 and question_count % 5 == 0:
            print("\n" + "─"*70)
            print(f"🎯 Milestone: {question_count} questions completed!")
            
            # Show quick stats
            session_summary = tracker.get_session_summary()
            if session_summary:
                print(f"   Overall Accuracy: {session_summary['accuracy_percentage']:.1f}%")
                
                velocity = session_summary['learning_velocity']
                if velocity['trend'] == 'improving':
                    print(f"   📈 You're improving! Keep it up!")
                elif velocity['trend'] == 'stable':
                    print(f"   ➡️  Steady progress - you're consistent!")
            
            print("─"*70)
            
            continue_choice = input("\n▶️  Continue? (yes/no): ").strip().lower()
            if continue_choice in ['no', 'n']:
                break
    
    # Step 4: Display comprehensive session summary
    print("\n" + "="*70)
    print("📊 FINAL SESSION REPORT")
    print("="*70)
    
    tracker.display_summary()
    
    # Show adaptation insights
    adaptation_summary = adaptive_engine.get_adaptation_summary()
    if adaptation_summary:
        print("\n🤖 ADAPTIVE SYSTEM INSIGHTS:")
        print(f"  Total Evaluations: {adaptation_summary['total_evaluations']}")
        print(f"  Difficulty Increases: {adaptation_summary['difficulty_increases']}")
        print(f"  Difficulty Decreases: {adaptation_summary['difficulty_decreases']}")
        print(f"  Average Confidence: {adaptation_summary['average_confidence']:.0%}")
    
    # Additional personalized insights
    summary = tracker.get_session_summary()
    if summary and summary['total_questions'] >= 3:
        print("\n💡 PERSONALIZED RECOMMENDATIONS:")
        
        if summary['accuracy_percentage'] >= 85:
            print("  ⭐ Outstanding! You're ready for more challenges!")
            print("  💪 Consider starting at a higher difficulty next time.")
        elif summary['accuracy_percentage'] >= 70:
            print("  👍 Great work! You're making solid progress.")
            print("  🎯 Focus on maintaining this consistency.")
        elif summary['accuracy_percentage'] >= 50:
            print("  📚 Good effort! Keep practicing to improve.")
            print("  💡 Try reviewing concepts at current difficulty.")
        else:
            print("  🌱 Every expert started as a beginner!")
            print("  📖 Consider reviewing fundamentals and practicing more.")
        
        # Speed feedback
        if summary['average_time'] < 5:
            print("  ⚡ You're very quick! Great mental math skills!")
        elif summary['average_time'] > 15:
            print("  🐢 Take your time, but try to build speed gradually.")
        
        # Operation-specific advice
        op_breakdown = summary['operation_breakdown']
        if len(op_breakdown) > 1:
            weakest_op = min(op_breakdown.items(), key=lambda x: x[1]['accuracy'])
            strongest_op = max(op_breakdown.items(), key=lambda x: x[1]['accuracy'])
            
            if weakest_op[1]['accuracy'] < 60:
                print(f"  📌 Focus area: {weakest_op[0].capitalize()} "
                      f"({weakest_op[1]['accuracy']:.0f}% accuracy)")
            
            if strongest_op[1]['accuracy'] >= 90:
                print(f"  ⭐ Strength: {strongest_op[0].capitalize()} "
                      f"({strongest_op[1]['accuracy']:.0f}% accuracy)")
    
    # Save session
    print()
    save_choice = input("💾 Save this session for future reference? (yes/no): ").strip().lower()
    if save_choice in ['yes', 'y']:
        tracker.save_session()
    
    print("\n" + "="*70)
    print("✨ Thank you for using Math Adventures! Keep learning! 🎉")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Session ended. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please restart the application.")
        import traceback
        traceback.print_exc()