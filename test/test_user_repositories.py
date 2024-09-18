import pytest
from model.User import User
from repository.database import create_tables, get_db_connection
from repository.user_repository import create_user, get_all_users, find_user_by_id, load_users, update_user, delete_user


@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    load_users()
    yield
    # Tear down - happens after tests are finished
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE trivia_user CASCADE")
    connection.commit()
    cursor.close()
    connection.close()


def test_create_fighter(setup_database):
    user = User(first="beni", last="talker", email="beni@gmail.com")
    new_id = create_user(user)
    assert new_id > 0


def test_get_all(setup_database):
    users = get_all_users()
    assert len(users) > 0
    assert isinstance(users[0], User)


def test_select_by_id(setup_database):
    user = find_user_by_id(1)
    assert user is not None
    assert isinstance(user, User)


def test_update_user(setup_database):
    user_id = 1
    updated_user = User(first="updated_first", last="updated_last", email="updated_email@gmail.com")
    update_success = update_user(user_id, updated_user)
    assert update_success
    user_after_update = find_user_by_id(user_id)
    assert user_after_update is not None
    assert user_after_update.first == "updated_first"
    assert user_after_update.last == "updated_last"
    assert user_after_update.email == "updated_email@gmail.com"


def test_delete_user(setup_database):
    user = User(first="to_delete", last="user", email="delete@gmail.com")
    new_id = create_user(user)
    created_user = find_user_by_id(new_id)
    assert created_user is not None
    delete_success = delete_user(new_id)
    assert delete_success
    deleted_user = find_user_by_id(new_id)
    assert deleted_user is None
