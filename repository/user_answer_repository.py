from datetime import timedelta
from typing import List
from model.UserAnswer import UserAnswer
from repository.database import get_db_connection


def create_user_answer(user_answer: UserAnswer) -> int:
    time_taken_str = str(user_answer.time_taken)
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO user_answer (user_id, question_id, answer_text, is_correct, time_taken) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (user_answer.user_id, user_answer.question_id, user_answer.answer_text, user_answer.is_correct,
             time_taken_str)
        )
        result = cursor.fetchone()
        if result is None:
            raise ValueError("No ID returned after user answer creation.")

        new_id = result.get('id')
        connection.commit()
        return new_id

def get_all_user_answers() -> List[UserAnswer]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_answer")
        res = cursor.fetchall()
        user_answers = [UserAnswer(**f) for f in res]
        return user_answers

def find_user_answer_by_id(user_answer_id: int) -> UserAnswer | None:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_answer WHERE id = %s", (user_answer_id,))
        result = cursor.fetchone()
        if result:
            time_taken = timedelta(seconds=result['time_taken'].total_seconds())
            return UserAnswer(
                user_id=result['user_id'],
                question_id=result['question_id'],
                answer_text=result['answer_text'],
                is_correct=result['is_correct'],
                time_taken=time_taken,
                id=result['id']
            )
        return None

def update_user_answer(user_answer_id: int, updated_user_answer: UserAnswer) -> bool:
    time_taken_str = str(updated_user_answer.time_taken)
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            UPDATE user_answer
            SET user_id = %s, question_id = %s, answer_text = %s, is_correct = %s, time_taken = %s
            WHERE id = %s
        """, (updated_user_answer.user_id, updated_user_answer.question_id, updated_user_answer.answer_text,
              updated_user_answer.is_correct, time_taken_str, user_answer_id))
        connection.commit()
        return cursor.rowcount > 0

def delete_user_answer(user_answer_id: int) -> bool:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM user_answer WHERE id = %s", (user_answer_id,))
        connection.commit()
        return cursor.rowcount > 0
