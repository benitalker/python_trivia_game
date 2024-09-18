import csv
from typing import List, Dict, Tuple
import statistics as s
from model.User import User
from model.Question import Question
from model.UserAnswer import UserAnswer
from repository.user_repository import get_all_users
from repository.question_repository import get_all_questions
from repository.user_answer_repository import get_all_user_answers


# Data fetching function remains the same as it's already functional
def get_data() -> Tuple[List[User], List[Question], List[UserAnswer]]:
    return get_all_users(), get_all_questions(), get_all_user_answers()


# Exercise 1: Find the highest scorer
def exercise_1(users: List[User], user_answers: List[UserAnswer]) -> Tuple[User, int]:
    user_scores = {
        answer.user_id: sum(1 for ans in user_answers if ans.is_correct and ans.user_id == answer.user_id)
        for answer in user_answers
    }

    highest_score_user_id = max(user_scores, key=user_scores.get, default=None)
    highest_score_user = next((user for user in users if user.id == highest_score_user_id), None)

    return highest_score_user, user_scores.get(highest_score_user_id, 0)


# Exercise 2: Find the question answered the fastest
def exercise_2(questions: List[Question], user_answers: List[UserAnswer]) -> Tuple[Question, float]:
    fastest_times = {
        q.id: min(
            (answer.time_taken.total_seconds() for answer in user_answers if
             answer.is_correct and answer.question_id == q.id),
            default=float('inf')
        )
        for q in questions
    }

    fastest_question_id = min(fastest_times, key=fastest_times.get, default=None)
    fastest_question = next((q for q in questions if q.id == fastest_question_id), None)

    return fastest_question, fastest_times.get(fastest_question_id, 0)


# Exercise 3: Find second place user by correctness and fastest time
def exercise_3(users: List[User], user_answers: List[UserAnswer]) -> Tuple[User, float]:
    user_scores = {
        user.id: {
            'correct': sum(1 for ans in user_answers if ans.is_correct and ans.user_id == user.id),
            'fastest': min((ans.time_taken.total_seconds() for ans in user_answers if ans.user_id == user.id),
                           default=float('inf'))
        }
        for user in users
    }

    sorted_users = sorted(user_scores.items(), key=lambda x: (x[1]['correct'], -x[1]['fastest']), reverse=True)

    second_place_user_id = sorted_users[1][0] if len(sorted_users) > 1 else None
    second_place_user = next((user for user in users if user.id == second_place_user_id), None)

    return second_place_user, user_scores.get(second_place_user_id, {}).get('fastest', 0)


# Exercise 4: Calculate the average time per question
def exercise_4(questions: List[Question], user_answers: List[UserAnswer]) -> Dict[int, float]:
    return {
        q.id: s.mean([ans.time_taken.total_seconds() for ans in user_answers if ans.question_id == q.id])
        if any(ans.question_id == q.id for ans in user_answers) else 0
        for q in questions
    }

# Exercise 5: Calculate the success rate for each question
def exercise_5(questions: List[Question], user_answers: List[UserAnswer]) -> Dict[int, float]:
    question_success = {q.id: {'correct': 0, 'total': 0} for q in questions}
    for answer in user_answers:
        question_success[answer.question_id]['total'] += 1
        if answer.is_correct:
            question_success[answer.question_id]['correct'] += 1

    return {
        q_id: (stats['correct'] / stats['total']) if stats['total'] > 0 else 0
        for q_id, stats in question_success.items()
    }



# Exercise 6: Find users who answered all questions
def exercise_6(users: List[User], questions: List[Question], user_answers: List[UserAnswer]) -> List[User]:
    return [
        user for user in users
        if len(set(ans.question_id for ans in user_answers if ans.user_id == user.id)) == len(questions)
    ]


# Exercise 7: Median time for correct and incorrect answers
def exercise_7(user_answers: List[UserAnswer]) -> Tuple[float, float]:
    correct_times = [ans.time_taken.total_seconds() for ans in user_answers if ans.is_correct]
    incorrect_times = [ans.time_taken.total_seconds() for ans in user_answers if not ans.is_correct]

    return (s.median(correct_times) if correct_times else 0, s.median(incorrect_times) if incorrect_times else 0)


# Exercise 8: Generate comprehensive user reports
def exercise_8(users: List[User], questions: List[Question], user_answers: List[UserAnswer]) -> List[Dict]:
    total_questions = len(questions)

    def generate_report(user: User) -> Dict:
        user_answers_for_user = [ans for ans in user_answers if ans.user_id == user.id]
        answered_questions = len(set(ans.question_id for ans in user_answers_for_user))
        correct_answers = sum(1 for ans in user_answers_for_user if ans.is_correct)
        times = [ans.time_taken.total_seconds() for ans in user_answers_for_user]

        return {
            'user_id': user.id,
            'name': f"{user.first} {user.last}",
            'total_questions': total_questions,
            'answered_questions': answered_questions,
            'correct_answers': correct_answers,
            'avg_time': s.mean(times) if times else 0,
            'fastest_answer': min(times) if times else 0,
            'slowest_answer': max(times) if times else 0,
            'unanswered_questions': total_questions - answered_questions
        }

    reports = list(map(generate_report, users))

    # Export to CSV
    with open('user_reports.csv', 'w', newline='') as csvfile:
        fieldnames = reports[0].keys() if reports else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reports)

    return reports


# Main function to call all exercises
def main():
    users, questions, user_answers = get_data()

    # Exercise 1
    highest_scorer, highest_score = exercise_1(users, user_answers)
    print(
        f"Exercise 1: Highest scorer is {highest_scorer.first if highest_scorer else 'None'} {highest_scorer.last if highest_scorer else ''} with {highest_score} correct answers.")

    # Exercise 2
    fastest_question, fastest_time = exercise_2(questions, user_answers)
    print(
        f"Exercise 2: Fastest question is '{fastest_question.question_text if fastest_question else 'None'}' answered in {fastest_time:.2f} seconds.")

    # Exercise 3
    second_place_user, fastest_time = exercise_3(users, user_answers)
    print(
        f"Exercise 3: Second place user is {second_place_user.first if second_place_user else 'None'} {second_place_user.last if second_place_user else ''} with a time of {fastest_time:.2f} seconds.")

    # Exercise 4
    avg_times = exercise_4(questions, user_answers)
    print("Exercise 4: Average time for each question:", avg_times)

    # Exercise 5
    success_rates = exercise_5(questions, user_answers)
    print("Exercise 5: Success rates for each question:", success_rates)

    # Exercise 6
    all_answered_users = exercise_6(users, questions, user_answers)
    print("Exercise 6: Users who answered all questions:", [f"{user.first} {user.last}" for user in all_answered_users])

    # Exercise 7
    correct_median, incorrect_median = exercise_7(user_answers)
    print(
        f"Exercise 7: Median time for correct answers: {correct_median:.2f}s, incorrect answers: {incorrect_median:.2f}s")

    # Exercise 8
    reports = exercise_8(users, questions, user_answers)
    print("Exercise 8: Reports exported to 'user_reports.csv'.")


if __name__ == "__main__":
    main()
