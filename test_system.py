"""
Enhanced Test Suite
Comprehensive testing for all components including new features:
- Confidence scoring
- Streak detection
- Dynamic windows
- Learning velocity
- Session persistence
"""

import sys
import os
sys.path.insert(0, 'src')

from puzzle_generator import PuzzleGenerator
from tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine

def print_test_header(test_name):
    """Print formatted test header"""
    print("\n" + "="*70)
    print(f"🧪 {test_name}")
    print("="*70)

def print_success(message):
    """Print success message"""
    print(f"  ✅ {message}")

def print_info(message):
    """Print info message"""
    print(f"  ℹ️  {message}")

def test_puzzle_generator():
    """Test puzzle generation for all difficulty levels"""
    print_test_header("Testing Puzzle Generator")
    gen = PuzzleGenerator()
    
    for difficulty in ['easy', 'medium', 'hard']:
        question, answer = gen.generate_puzzle(difficulty)
        print_info(f"{difficulty.upper()}: {question} = {answer}")
        assert answer is not None, f"Answer should not be None for {difficulty}"
    
    print_success("Puzzle Generator works correctly!")
    return True

def test_performance_tracker():
    """Test enhanced performance tracking"""
    print_test_header("Testing Enhanced Performance Tracker")
    tracker = PerformanceTracker("TestUser")
    
    # Simulate attempts
    tracker.record_attempt("5 + 3", 8, 8, 2.5, "easy")
    tracker.record_attempt("7 + 2", 9, 9, 3.0, "easy")
    tracker.record_attempt("4 + 6", 10, 10, 2.0, "easy")
    tracker.record_attempt("8 × 5", 40, 40, 4.5, "medium")
    
    # Test metrics
    metrics = tracker.get_recent_performance(3)
    print_info(f"Accuracy: {metrics['accuracy']*100:.0f}%")
    print_info(f"Avg Time: {metrics['avg_time']:.1f}s")
    assert metrics['accuracy'] == 1.0, "All answers correct, should be 100%"
    
    # Test operation breakdown
    op_breakdown = tracker.get_operation_breakdown()
    print_info(f"Operations tracked: {list(op_breakdown.keys())}")
    assert 'addition' in op_breakdown, "Should track addition"
    
    # Test learning velocity
    for i in range(6):  # Add more attempts for velocity calculation
        tracker.record_attempt(f"Q{i}", i, i, 3.0, "easy")
    
    velocity = tracker.get_learning_velocity()
    print_info(f"Learning trend: {velocity['trend']}")
    
    print_success("Performance Tracker works correctly!")
    return True

def test_confidence_scoring():
    """Test confidence calculation"""
    print_test_header("Testing Confidence Scoring")
    engine = AdaptiveEngine()
    
    # Test Case 1: High confidence (consistent, accurate)
    high_perf = {
        'accuracy': 0.9,
        'avg_time': 4.0,
        'total_attempts': 3,
        'times': [4.0, 4.1, 3.9]
    }
    attempts = [True, True, True]
    confidence = engine.calculate_confidence_score(high_perf, attempts)
    print_info(f"High performance confidence: {confidence:.2f}")
    assert confidence > 0.7, "High performance should have high confidence"
    
    # Test Case 2: Low confidence (inconsistent)
    low_perf = {
        'accuracy': 0.5,
        'avg_time': 8.0,
        'total_attempts': 4,
        'times': [3.0, 15.0, 5.0, 12.0]  # High variance
    }
    attempts = [True, False, True, False]  # Alternating pattern
    confidence = engine.calculate_confidence_score(low_perf, attempts)
    print_info(f"Inconsistent performance confidence: {confidence:.2f}")
    assert confidence < 0.6, "Inconsistent performance should have low confidence"
    
    print_success("Confidence Scoring works correctly!")
    return True

def test_streak_detection():
    """Test hot/cold streak detection"""
    print_test_header("Testing Streak Detection")
    engine = AdaptiveEngine()
    
    # Test hot streak
    hot_streak = [True, True, True, True]
    streak_info = engine.detect_streak(hot_streak)
    print_info(f"Hot streak: {streak_info}")
    assert streak_info['type'] == 'hot', "Should detect hot streak"
    assert streak_info['is_significant'], "4 correct should be significant"
    assert streak_info['length'] == 4, "Streak length should be 4"
    
    # Test cold streak
    cold_streak = [False, False, False]
    streak_info = engine.detect_streak(cold_streak)
    print_info(f"Cold streak: {streak_info}")
    assert streak_info['type'] == 'cold', "Should detect cold streak"
    assert streak_info['is_significant'], "3 incorrect should be significant"
    
    # Test no streak
    no_streak = [True, False, True]
    streak_info = engine.detect_streak(no_streak)
    print_info(f"No streak: {streak_info}")
    assert not streak_info['is_significant'], "Alternating should not be significant"
    
    print_success("Streak Detection works correctly!")
    return True

def test_dynamic_window():
    """Test dynamic window sizing"""
    print_test_header("Testing Dynamic Window Sizing")
    engine = AdaptiveEngine()
    
    # Easy difficulty + high confidence = small window
    window1 = engine.get_dynamic_window('easy', 0.9)
    print_info(f"Easy + High Confidence: {window1} questions")
    assert window1 <= 3, "Should have small window"
    
    # Hard difficulty + low confidence = large window
    window2 = engine.get_dynamic_window('hard', 0.3)
    print_info(f"Hard + Low Confidence: {window2} questions")
    assert window2 >= 4, "Should have large window"
    
    # Medium difficulty + medium confidence = standard window
    window3 = engine.get_dynamic_window('medium', 0.6)
    print_info(f"Medium + Medium Confidence: {window3} questions")
    assert 2 <= window3 <= 5, "Should be within range"
    
    print_success("Dynamic Window Sizing works correctly!")
    return True

def test_adaptive_engine_decisions():
    """Test enhanced adaptive engine decisions"""
    print_test_header("Testing Enhanced Adaptive Engine Decisions")
    engine = AdaptiveEngine()
    
    # Test Case 1: High performance with hot streak
    high_perf = {
        'accuracy': 0.95,
        'avg_time': 3.5,
        'total_attempts': 4,
        'times': [3.2, 3.5, 3.6, 3.7]
    }
    attempts = [True, True, True, True]
    
    next_diff, details = engine.decide_next_difficulty(
        'easy', high_perf, attempts, 4
    )
    print_info(f"High performance: {next_diff} (from easy)")
    print_info(f"Confidence: {details['confidence']:.2f}")
    print_info(f"Factors: {', '.join(details['factors'][:2])}")
    assert next_diff == 'medium', "Should increase difficulty"
    assert details['confidence'] > 0.7, "Should have high confidence"
    
    # Test Case 2: Low performance
    low_perf = {
        'accuracy': 0.4,
        'avg_time': 12.0,
        'total_attempts': 3,
        'times': [10.0, 12.0, 14.0]
    }
    attempts = [False, False, True]
    
    next_diff, details = engine.decide_next_difficulty(
        'medium', low_perf, attempts, 3
    )
    print_info(f"Low performance: {next_diff} (from medium)")
    print_info(f"Adjustment score: {details['adjustment_score']:.1f}")
    assert next_diff == 'easy', "Should decrease difficulty"
    
    # Test Case 3: Steady performance (maintain)
    steady_perf = {
        'accuracy': 0.7,
        'avg_time': 8.0,
        'total_attempts': 3,
        'times': [7.5, 8.0, 8.5]
    }
    attempts = [True, True, False]
    
    next_diff, details = engine.decide_next_difficulty(
        'medium', steady_perf, attempts, 3
    )
    print_info(f"Steady performance: {next_diff} (from medium)")
    assert next_diff == 'medium', "Should maintain difficulty"
    
    print_success("Adaptive Engine Decisions work correctly!")
    return True

def test_session_persistence():
    """Test session saving and loading"""
    print_test_header("Testing Session Persistence")
    
    # Create and populate tracker
    tracker = PerformanceTracker("PersistenceTest")
    for i in range(5):
        tracker.record_attempt(f"Q{i}", i, i, 3.0 + i*0.5, "easy")
    
    # Save session
    filename = tracker.save_session()
    print_info(f"Session saved: {filename}")
    assert filename is not None, "Should save successfully"
    assert os.path.exists(filename), "File should exist"
    
    # Load session
    loaded_data = PerformanceTracker.load_session(filename)
    print_info(f"Session loaded: {loaded_data['username']}")
    assert loaded_data is not None, "Should load successfully"
    assert loaded_data['username'] == "PersistenceTest", "Username should match"
    assert loaded_data['total_questions'] == 5, "Question count should match"
    
    # Clean up
    if os.path.exists(filename):
        os.remove(filename)
        print_info("Test file cleaned up")
    
    print_success("Session Persistence works correctly!")
    return True

def test_integration_scenario():
    """Test realistic learning scenario"""
    print_test_header("Testing Complete Learning Scenario")
    
    gen = PuzzleGenerator()
    tracker = PerformanceTracker("IntegrationTest")
    engine = AdaptiveEngine()
    
    current_difficulty = 'easy'
    attempts_since_adjustment = 0
    
    print_info("Simulating 12-question session...")
    
    # Simulate improving student
    for i in range(12):
        question, answer = gen.generate_puzzle(current_difficulty)
        
        # Simulate mostly correct answers (90% accuracy)
        is_correct = (i % 10 != 0)  # Wrong on questions 0 and 10
        user_answer = answer if is_correct else answer + 1
        time_taken = 3.0 + (i % 3)  # Varying times
        
        tracker.record_attempt(
            question, user_answer, answer, 
            time_taken, current_difficulty
        )
        attempts_since_adjustment += 1
        
        # Check for difficulty adjustment every 3 questions
        if attempts_since_adjustment >= 3:
            recent = tracker.get_recent_performance(3)
            old_diff = current_difficulty
            
            current_difficulty, details = engine.decide_next_difficulty(
                current_difficulty,
                recent,
                recent['attempts_list'],
                attempts_since_adjustment
            )
            
            if old_diff != current_difficulty:
                print_info(f"Q{i+1}: {old_diff} → {current_difficulty} "
                          f"(confidence: {details['confidence']:.0%})")
                attempts_since_adjustment = 0
    
    # Get final summary
    summary = tracker.get_session_summary()
    print_info(f"Final accuracy: {summary['accuracy_percentage']:.0f}%")
    print_info(f"Final difficulty: {summary['final_difficulty']}")
    print_info(f"Learning trend: {summary['learning_velocity']['trend']}")
    
    # Verify progression
    assert summary['final_difficulty'] != 'easy', "Should have progressed beyond easy"
    assert summary['accuracy_percentage'] >= 80, "Should maintain high accuracy"
    
    print_success("Integration Scenario passed!")
    return True

def test_edge_cases():
    """Test edge cases and error handling"""
    print_test_header("Testing Edge Cases")
    
    engine = AdaptiveEngine()
    
    # Test with minimal data
    minimal_perf = {
        'accuracy': 1.0,
        'avg_time': 5.0,
        'total_attempts': 1,
        'times': [5.0]
    }
    attempts = [True]
    
    next_diff, details = engine.decide_next_difficulty(
        'easy', minimal_perf, attempts, 1
    )
    print_info(f"Minimal data: {next_diff} (should maintain)")
    assert next_diff == 'easy', "Should maintain with insufficient data"
    
    # Test at boundaries
    boundary_perf = {
        'accuracy': 1.0,
        'avg_time': 3.0,
        'total_attempts': 5,
        'times': [3.0, 3.0, 3.0, 3.0, 3.0]
    }
    attempts = [True, True, True, True, True]
    
    # Already at hardest
    next_diff, _ = engine.decide_next_difficulty(
        'hard', boundary_perf, attempts, 5
    )
    print_info(f"At max difficulty: {next_diff} (should stay hard)")
    assert next_diff == 'hard', "Cannot go above hard"
    
    # Already at easiest
    low_perf = {
        'accuracy': 0.2,
        'avg_time': 20.0,
        'total_attempts': 5,
        'times': [20.0] * 5
    }
    attempts = [False] * 5
    
    next_diff, _ = engine.decide_next_difficulty(
        'easy', low_perf, attempts, 5
    )
    print_info(f"At min difficulty: {next_diff} (should stay easy)")
    assert next_diff == 'easy', "Cannot go below easy"
    
    print_success("Edge Cases handled correctly!")
    return True

def run_all_tests():
    """Run comprehensive test suite"""
    print("\n" + "🚀 "*35)
    print("🧪 RUNNING ENHANCED TEST SUITE")
    print("🚀 "*35)
    
    tests = [
        ("Puzzle Generator", test_puzzle_generator),
        ("Performance Tracker", test_performance_tracker),
        ("Confidence Scoring", test_confidence_scoring),
        ("Streak Detection", test_streak_detection),
        ("Dynamic Window", test_dynamic_window),
        ("Adaptive Engine", test_adaptive_engine_decisions),
        ("Session Persistence", test_session_persistence),
        ("Integration Scenario", test_integration_scenario),
        ("Edge Cases", test_edge_cases)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            failed += 1
            print(f"\n  ❌ FAILED: {e}")
        except Exception as e:
            failed += 1
            print(f"\n  ❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    # Print summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    print(f"  Total Tests: {len(tests)}")
    print(f"  ✅ Passed: {passed}")
    print(f"  ❌ Failed: {failed}")
    print(f"  Success Rate: {(passed/len(tests)*100):.0f}%")
    print("="*70)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\n✨ Your enhanced adaptive learning system is ready!")
        print("📦 Run: python src/main.py")
        print("\n" + "="*70 + "\n")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)