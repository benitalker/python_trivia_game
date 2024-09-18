import csv
from typing import List, Dict, Tuple
import statistics as s
from model.User import User
from model.Question import Question
from model.UserAnswer import UserAnswer
from repository.user_repository import get_all_users
from repository.question_repository import get_all_questions
from repository.user_answer_repository import get_all_user_answers


def get_data() -> Tuple[List[User], List[Question], List[UserAnswer]]:
    users = get_all_users()
    questions = get_all_questions()
    user_answers = get_all_user_answers()
    return users, questions, user_answers


def exercise_1(users: List[User], user_answers: List[UserAnswer]) -> Tuple[User, int]:
    user_scores = {user.id: 0 for user in users}
    for answer in user_answers:
        if answer.is_correct:
            user_scores[answer.user_id] += 1

    if not user_scores:
        return None, 0

    highest_score_user_id = max(user_scores, key=user_scores.get)
    highest_score_user = next(user for user in users if user.id == highest_score_user_id)
    return highest_score_user, user_scores[highest_score_user_id]


def exercise_2(questions: List[Question], user_answers: List[UserAnswer]) -> Tuple[Question, float]:
    question_times = {q.id: [] for q in questions}
    for answer in user_answers:
        if answer.is_correct:
            question_times[answer.question_id].append(answer.time_taken.total_seconds())

    fastest_times = {q_id: min(times) if times else float('inf') for q_id, times in question_times.items()}
    if not fastest_times:
        return None, 0

    fastest_question_id = min(fastest_times, key=fastest_times.get)
    fastest_question = next(q for q in questions if q.id == fastest_question_id)
    fastest_time = fastest_times[fastest_question_id]
    return fastest_question, fastest_time


def exercise_3(users: List[User], user_answers: List[UserAnswer]) -> Tuple[User, float]:
    user_scores = {user.id: {'correct': 0, 'fastest': float('inf')} for user in users}
    for answer in user_answers:
        if answer.is_correct:
            user_scores[answer.user_id]['correct'] += 1
        user_scores[answer.user_id]['fastest'] = min(user_scores[answer.user_id]['fastest'],
                                                     answer.time_taken.total_seconds())

    sorted_users = sorted(user_scores.items(), key=lambda x: (x[1]['correct'], -x[1]['fastest']), reverse=True)
    if len(sorted_users) < 2:
        return None, 0

    second_place_user_id = sorted_users[1][0]
    second_place_user = next(user for user in users if user.id == second_place_user_id)
    return second_place_user, user_scores[second_place_user_id]['fastest']


def exercise_4(questions: List[Question], user_answers: List[UserAnswer]) -> Dict[int, float]:
    question_times = {q.id: [] for q in questions}
    for answer in user_answers:
        question_times[answer.question_id].append(answer.time_taken.total_seconds())

    return {q_id: s.mean(times) if times else 0 for q_id, times in question_times.items()}


def exercise_5(questions: List[Question], user_answers: List[UserAnswer]) -> Dict[int, float]:
    question_success = {q.id: {'correct': 0, 'total': 0} for q in questions}
    for answer in user_answers:
        question_success[answer.question_id]['total'] += 1
        if answer.is_correct:
            question_success[answer.question_id]['correct'] += 1

    return {q_id: stats['correct'] / stats['total'] if stats['total'] > 0 else 0
            for q_id, stats in question_success.items()}


def exercise_6(users: List[User], questions: List[Question], user_answers: List[UserAnswer]) -> List[User]:
    question_count = len(questions)
    user_answer_counts = {user.id: set() for user in users}
    for answer in user_answers:
        user_answer_counts[answer.user_id].add(answer.question_id)

    return [user for user in users if len(user_answer_counts[user.id]) == question_count]


def exercise_7(user_answers: List[UserAnswer]) -> Tuple[float, float]:
    correct_times = [answer.time_taken.total_seconds() for answer in user_answers if answer.is_correct]
    incorrect_times = [answer.time_taken.total_seconds() for answer in user_answers if not answer.is_correct]

    return (s.median(correct_times) if correct_times else 0,
            s.median(incorrect_times) if incorrect_times else 0)


def exercise_8(users: List[User], questions: List[Question], user_answers: List[UserAnswer]) -> List[Dict]:
    reports = []
    total_questions = len(questions)

    for user in users:
        user_report = {
            'user_id': user.id,
            'name': f"{user.first} {user.last}",
            'total_questions': total_questions,
            'answered_questions': 0,
            'correct_answers': 0,
            'avg_time': 0,
            'fastest_answer': float('inf'),
            'slowest_answer': 0,
            'unanswered_questions': total_questions
        }

        user_times = []
        for answer in user_answers:
            if answer.user_id == user.id:
                user_report['answered_questions'] += 1
                user_report['unanswered_questions'] -= 1
                time_taken = answer.time_taken.total_seconds()
                user_times.append(time_taken)
                user_report['fastest_answer'] = min(user_report['fastest_answer'], time_taken)
                user_report['slowest_answer'] = max(user_report['slowest_answer'], time_taken)
                if answer.is_correct:
                    user_report['correct_answers'] += 1

        user_report['avg_time'] = s.mean(user_times) if user_times else 0
        user_report['fastest_answer'] = user_report['fastest_answer'] if user_report['fastest_answer'] != float(
            'inf') else 0

        reports.append(user_report)

    # Export to CSV
    with open('user_reports.csv', 'w', newline='') as csvfile:
        fieldnames = reports[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for report in reports:
            writer.writerow(report)

    return reports


def main():
    users, questions, user_answers = get_data()

    # Exercise 1
    highest_scorer, highest_score = exercise_1(users, user_answers)
    if highest_scorer:
        print(
            f"Exercise 1: Highest scorer is {highest_scorer.first} {highest_scorer.last} with {highest_score} correct answers.")
    else:
        print("Exercise 1: No data available for highest scorer.")

    # Exercise 2
    fastest_question, fastest_time = exercise_2(questions, user_answers)
    if fastest_question:
        print(
            f"Exercise 2: Question answered correctly the fastest is '{fastest_question.question_text}' in {fastest_time:.2f} seconds.")
    else:
        print("Exercise 2: No data available for fastest answered question.")

    # Exercise 3
    second_place_user, fastest_time = exercise_3(users, user_answers)
    if second_place_user:
        print(
            f"Exercise 3: Second-place user is {second_place_user.first} {second_place_user.last} with fastest answer time of {fastest_time:.2f} seconds.")
    else:
        print("Exercise 3: Not enough data to determine second-place user.")

    # Exercise 4
    avg_times = exercise_4(questions, user_answers)
    print("Exercise 4: Average time taken for each question:")
    for q_id, avg_time in avg_times.items():
        print(f"Question ID {q_id}: {avg_time:.2f} seconds")

    # Exercise 5
    success_rates = exercise_5(questions, user_answers)
    print("Exercise 5: Success rate for each question:")
    for q_id, rate in success_rates.items():
        print(f"Question ID {q_id}: {rate * 100:.2f}%")

    # Exercise 6
    all_answered_users = exercise_6(users, questions, user_answers)
    if all_answered_users:
        print("Exercise 6: Users who have answered all questions:")
        for user in all_answered_users:
            print(f"{user.first} {user.last}")
    else:
        print("Exercise 6: No users have answered all questions.")

    # Exercise 7
    correct_median, incorrect_median = exercise_7(user_answers)
    print(
        f"Exercise 7: Median time for correct answers: {correct_median:.2f} seconds, incorrect answers: {incorrect_median:.2f} seconds")

    # Exercise 8
    reports = exercise_8(users, questions, user_answers)
    print("Exercise 8: Comprehensive reports generated and exported to 'user_reports.csv'")


if __name__ == "__main__":
    main()