from typing import List
import requests
from model.Question import Question
from model.Answer import Answer


def fetch_questions() -> List[tuple[Question, List[Answer]]]:
    response = requests.get("https://opentdb.com/api.php?amount=20")
    data = response.json()
    question_answer_pairs = []

    for q_data in data['results']:
        question = Question(
            question_text=q_data['question'],
            correct_answer=q_data['correct_answer']
        )

        incorrect_answers = [
            Answer(question_id=None, incorrect_answer=a_data)
            for a_data in q_data['incorrect_answers']
        ]

        question_answer_pairs.append((question, incorrect_answers))

    return question_answer_pairs