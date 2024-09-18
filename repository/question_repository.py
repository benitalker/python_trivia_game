from typing import List
from model.Question import Question
from repository.database import get_db_connection


def create_question(question: Question) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO question (question_text, correct_answer) VALUES (%s, %s) RETURNING id",
            (question.question_text, question.correct_answer)
        )
        result = cursor.fetchone()
        if result is None:
            raise ValueError("No ID returned after question creation.")

        new_id = result.get('id')
        connection.commit()
        return new_id

def get_all_questions() -> List[Question]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM question""")
        res = cursor.fetchall()
        questions = [Question(**f) for f in res]
        return questions

def find_question_by_id(question_id: int) -> Question | None:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM question WHERE id = %s", (question_id,))
        result = cursor.fetchone()
        if result is None:
            return None
        return Question(**result)

def update_question(question_id: int, updated_question: Question) -> bool:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            UPDATE question
            SET question_text = %s, correct_answer = %s
            WHERE id = %s
        """, (updated_question.question_text, updated_question.correct_answer, question_id))

        connection.commit()
        return cursor.rowcount > 0

def delete_question(question_id: int) -> bool:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM question WHERE id = %s", (question_id,))
        connection.commit()
        return cursor.rowcount > 0
