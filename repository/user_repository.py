from core.database import get_connection


def create_user(cognito_sub, username, email):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users
                (
                    cognito_sub,
                    name,
                    email
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
                """,
                (cognito_sub, username, email),
            )

        conn.commit()

    finally:
        conn.close()


def get_user_by_id(user_id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM users
                WHERE id = %s
                """,
                (user_id,),
            )
            return cur.fetchone()

    finally:
        conn.close()

def get_user_by_cognito_sub(cognito_sub):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM users
                WHERE cognito_sub = %s
                """,
                (cognito_sub,),
            )
            return cur.fetchone()

    finally:
        conn.close()