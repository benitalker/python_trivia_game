import pytest
from model.Question import Question
from repository.database import create_tables, get_db_connection
from repository.question_repository import create_question, get_all_questions, find_question_by_id, update_question, \
    delete_question

@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    yield
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE question CASCADE")
    connection.commit()
    cursor.close()
    connection.close()

def test_create_question(setup_database):
    question = Question(question_text="What is 2 + 2?", correct_answer="4")
    new_id = create_question(question)
    assert new_id > 0

def test_get_all_questions(setup_database):
    question = Question(question_text="What is the capital of France?", correct_answer="Paris")
    create_question(question)
    questions = get_all_questions()
    assert len(questions) > 0
    assert isinstance(questions[0], Question)

def test_find_question_by_id(setup_database):
    question = Question(question_text="What is 3 + 5?", correct_answer="8")
    new_id = create_question(question)
    found_question = find_question_by_id(new_id)
    assert found_question is not None
    assert found_question.question_text == "What is 3 + 5?"
    assert found_question.correct_answer == "8"

def test_update_question(setup_database):
    question = Question(question_text="What is the color of the sky?", correct_answer="Blue")
    new_id = create_question(question)
    updated_question = Question(question_text="What is the color of grass?", correct_answer="Green")
    update_success = update_question(new_id, updated_question)
    assert update_success
    updated_question_in_db = find_question_by_id(new_id)
    assert updated_question_in_db is not None
    assert updated_question_in_db.question_text == "What is the color of grass?"
    assert updated_question_in_db.correct_answer == "Green"

def test_delete_question(setup_database):
    question = Question(question_text="What is 10 - 7?", correct_answer="3")
    new_id = create_question(question)
    created_question = find_question_by_id(new_id)
    assert created_question is not None
    delete_success = delete_question(new_id)
    assert delete_success
    deleted_question = find_question_by_id(new_id)
    assert deleted_question is None
