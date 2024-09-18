from api.question_api import fetch_questions
from repository.answer_repository import create_answer
from repository.database import is_tables_exists, create_tables
from repository.question_repository import create_question
from repository.user_repository import load_users


def seed():
    if not is_tables_exists():
        create_tables()
        load_users()
        question_answer_pairs = fetch_questions()
        for question, incorrect_answers in question_answer_pairs:
            question_id = create_question(question)
            for answer in incorrect_answers:
                answer.question_id = question_id
                create_answer(answer)
