import psycopg2
from psycopg2.extras import RealDictCursor
from config.sql_config import SQL_URI


def get_db_connection():
    return psycopg2.connect(SQL_URI, cursor_factory=RealDictCursor)

def create_tables():
    _create_table_trivia_user()
    _create_table_question()
    _create_table_answer()
    _create_table_user_answer()

def _create_table_trivia_user():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trivia_user (
            id SERIAL PRIMARY KEY,
            first VARCHAR(100) NOT NULL,
            last VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
        ''')
        connection.commit()

def _create_table_question():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS question (
            id SERIAL PRIMARY KEY,
            question_text TEXT NOT NULL,
            correct_answer VARCHAR(255) NOT NULL
        )
        ''')
        connection.commit()

def _create_table_answer():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS answer (
            id SERIAL PRIMARY KEY,
            question_id INTEGER NOT NULL,
            incorrect_answer VARCHAR(255) NOT NULL,
            FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE
        )
        ''')
        connection.commit()

def _create_table_user_answer():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_answer (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            answer_text VARCHAR(255) NOT NULL,
            is_correct BOOLEAN NOT NULL,
            time_taken INTERVAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES trivia_user(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE
        )
        ''')
        connection.commit()


def is_tables_exists() -> bool:
    table_names = ['trivia_user', 'question', 'answer', 'user_answer']
    existing_tables = []

    with get_db_connection() as connection, connection.cursor() as cursor:
        for table_name in table_names:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                );
            """, (table_name,))

            if cursor.fetchone()['exists']:
                existing_tables.append(table_name)
    print("The following tables exist:", ", ".join(existing_tables))
    if set(existing_tables) == set(table_names):
        print("All tables have been created successfully.")
        return True
    else:
        print("Missing tables:", ", ".join(set(table_names) - set(existing_tables)))
        return False


def drop_all_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
        DROP TABLE IF EXISTS user_answer;
        DROP TABLE IF EXISTS answer;
        DROP TABLE IF EXISTS question;
        DROP TABLE IF EXISTS trivia_user;
    ''')

    connection.commit()
    cursor.close()
    connection.close()
    