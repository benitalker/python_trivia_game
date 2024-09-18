from typing import List

from api.user_api import fetch_users
from model.User import User
from repository.database import get_db_connection

def load_users():
    users = fetch_users()
    for user in users:
        create_user(user)

# create
def create_user(user: User) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO trivia_user (first, last, email) VALUES (%s, %s, %s) RETURNING id",
                (user.first, user.last,user.email)
            )
            result = cursor.fetchone()
            if result is None:
                raise ValueError("No ID returned after user creation.")
            new_id = result.get('id')
            connection.commit()
            return new_id

# getAll
def get_all_users() -> List[User]:
    with get_db_connection() as connection, connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM trivia_user""")
            res = cursor.fetchall()
            users = [User(**f) for f in res]
            return users

# findById
def find_user_by_id(user_id: int) -> User | None:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM trivia_user WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if result is None:
            return None
        return User(**result)

# update
def update_user(user_id: int, updated_user: User) -> bool:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            UPDATE trivia_user
            SET first = %s, last = %s, email = %s
            WHERE id = %s
        """, (updated_user.first, updated_user.last, updated_user.email, user_id))
        connection.commit()
        return cursor.rowcount > 0

# delete
def delete_user(user_id: int) -> bool:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM trivia_user WHERE id = %s", (user_id,))
        connection.commit()
        return cursor.rowcount > 0
