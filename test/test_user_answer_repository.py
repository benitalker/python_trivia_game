from datetime import timedelta

import pytest
from model.UserAnswer import UserAnswer
from repository.database import create_tables, get_db_connection
from repository.user_answer_repository import create_user_answer, get_all_user_answers, find_user_answer_by_id, update_user_answer, delete_user_answer


@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    yield
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE user_answer CASCADE")
    connection.commit()
    cursor.close()
    connection.close()

def test_create_user_answer(setup_database):
    user_answer = UserAnswer(user_id=1, question_id=1, answer_text="Sample Answer", is_correct=True,
                             time_taken=timedelta(seconds=5))
    new_id = create_user_answer(user_answer)
    assert new_id > 0

def test_get_all_user_answers(setup_database):
    user_answer = UserAnswer(user_id=1, question_id=1, answer_text="Sample Answer", is_correct=True, time_taken=5.0)
    create_user_answer(user_answer)
    user_answers = get_all_user_answers()
    assert len(user_answers) > 0
    assert isinstance(user_answers[0], UserAnswer)

def test_find_user_answer_by_id(setup_database):
    user_answer = UserAnswer(user_id=1, question_id=1, answer_text="Another Sample Answer", is_correct=False, time_taken=timedelta(seconds=10))
    new_id = create_user_answer(user_answer)
    found_user_answer = find_user_answer_by_id(new_id)
    assert found_user_answer is not None
    assert found_user_answer.user_id == 1
    assert found_user_answer.question_id == 1
    assert found_user_answer.answer_text == "Another Sample Answer"
    assert found_user_answer.is_correct is False
    assert found_user_answer.time_taken == timedelta(seconds=10)

def test_update_user_answer(setup_database):
    user_answer = UserAnswer(user_id=1, question_id=1, answer_text="Old Answer", is_correct=True, time_taken=5.0)
    new_id = create_user_answer(user_answer)
    updated_user_answer = UserAnswer(user_id=1, question_id=1, answer_text="Updated Answer", is_correct=False, time_taken=8.0)
    update_success = update_user_answer(new_id, updated_user_answer)
    assert update_success
    updated_user_answer_in_db = find_user_answer_by_id(new_id)
    assert updated_user_answer_in_db is not None
    assert updated_user_answer_in_db.answer_text == "Updated Answer"
    assert updated_user_answer_in_db.is_correct is False
    assert updated_user_answer_in_db.time_taken == timedelta(seconds=8)


def test_delete_user_answer(setup_database):
    user_answer = UserAnswer(user_id=1, question_id=1, answer_text="Delete Me", is_correct=True, time_taken=5.0)
    new_id = create_user_answer(user_answer)
    created_user_answer = find_user_answer_by_id(new_id)
    assert created_user_answer is not None
    delete_success = delete_user_answer(new_id)
    assert delete_success
    deleted_user_answer = find_user_answer_by_id(new_id)
    assert deleted_user_answer is None
