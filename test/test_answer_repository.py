import pytest
from model.Answer import Answer
from repository.database import create_tables, get_db_connection
from repository.answer_repository import create_answer, get_all_answers, find_answer_by_id, update_answer, delete_answer


@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    yield
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE answer CASCADE")
    connection.commit()
    cursor.close()
    connection.close()


def test_create_answer(setup_database):
    answer = Answer(question_id=1, incorrect_answer="Wrong Answer")
    new_id = create_answer(answer)
    assert new_id > 0


def test_get_all_answers(setup_database):
    answer = Answer(question_id=1, incorrect_answer="Wrong Answer")
    create_answer(answer)
    answers = get_all_answers()
    assert len(answers) > 0
    assert isinstance(answers[0], Answer)


def test_find_answer_by_id(setup_database):
    answer = Answer(question_id=1, incorrect_answer="Another Wrong Answer")
    new_id = create_answer(answer)
    found_answer = find_answer_by_id(new_id)
    assert found_answer is not None
    assert found_answer.question_id == 1
    assert found_answer.incorrect_answer == "Another Wrong Answer"


def test_update_answer(setup_database):
    answer = Answer(question_id=1, incorrect_answer="Old Answer")
    new_id = create_answer(answer)
    updated_answer = Answer(question_id=1, incorrect_answer="Updated Answer")
    update_success = update_answer(new_id, updated_answer)
    assert update_success
    updated_answer_in_db = find_answer_by_id(new_id)
    assert updated_answer_in_db is not None
    assert updated_answer_in_db.incorrect_answer == "Updated Answer"


def test_delete_answer(setup_database):
    answer = Answer(question_id=1, incorrect_answer="Delete Me")
    new_id = create_answer(answer)
    created_answer = find_answer_by_id(new_id)
    assert created_answer is not None
    delete_success = delete_answer(new_id)
    assert delete_success
    deleted_answer = find_answer_by_id(new_id)
    assert deleted_answer is None
