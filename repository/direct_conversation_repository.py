from core.database import get_connection

def create_direct_conversation(user1_id, user2_id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO direct_conversations
                (
                    user_one_id,
                    user_two_id
                )
                VALUES
                (
                    %s,
                    %s
                )
                RETURNING id
                """,
                (user1_id, user2_id),
            )
            conversation = cur.fetchone()

        conn.commit()
        return conversation

    finally:
        conn.close()

def get_direct_conversation(user1_id, user2_id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM direct_conversations
                WHERE user_one_id = %s AND user_two_id = %s
                """,
                (user1_id, user2_id),
            )
            return cur.fetchall()

    finally:
        conn.close()

def get_user_by_email(email):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM users
                WHERE email = %s
                """,
                (email,),
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

def get_direct_conversations_for_user(user_id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM direct_conversations
                WHERE user_one_id = %s OR user_two_id = %s
                """,
                (user_id, user_id),
            )
            return cur.fetchall()

    finally:
        conn.close()

def get_direct_conversation_by_id(id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM direct_conversations
                WHERE id = %s
                """,
                (id,),
            )
            return cur.fetchone()

    finally:
        conn.close()