from typing import List

from model.Answer import Answer
from repository.database import get_db_connection


def create_answer(answer: Answer) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO answer (question_id, incorrect_answer) VALUES (%s, %s) RETURNING id",
            (answer.question_id, answer.incorrect_answer)
        )
        result = cursor.fetchone()
        if result is None:
            raise ValueError("No ID returned after answer creation.")
        new_id = result.get('id')
        connection.commit()
        return new_id

def get_all_answers(question_id:int) -> List[Answer]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM answer")
        res = cursor.fetchall()
        answers = [Answer(**f) for f in res]
        return list(filter(lambda ans: ans.question_id == question_id,answers))

def find_answer_by_id(answer_id: int) -> Answer:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM answer WHERE id = %s", (answer_id,))
        result = cursor.fetchone()
        return Answer(**result) if result else None

def update_answer(answer_id: int, updated_answer: Answer) -> bool:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            UPDATE answer
            SET question_id = %s, 
            incorrect_answer = %s
            WHERE id = %s
        """,
        (updated_answer.question_id, updated_answer.incorrect_answer, answer_id)
        )
        connection.commit()
        return cursor.rowcount > 0

def delete_answer(answer_id: int) -> bool:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM answer WHERE id = %s", (answer_id,))
        connection.commit()
        return cursor.rowcount > 0
