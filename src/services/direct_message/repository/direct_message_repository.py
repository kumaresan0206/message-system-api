from common.database.database import get_connection

def create_direct_message(conversation_id, sender_id, content):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO direct_messages
                (
                    direct_conversation_id,
                    sender_id,
                    content
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
                RETURNING id
                """,
                (conversation_id, sender_id, content),
            )

            message_id = cur.fetchone()[0]

        conn.commit()

        return message_id

    finally:
        conn.close()


def get_direct_conversation_by_id(conversation_id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM direct_conversations
                WHERE id = %s
                """,
                (conversation_id,),
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

def get_messages_by_conversation_id(conversation_id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, direct_conversation_id, sender_id, content, created_at
                FROM direct_messages
                WHERE direct_conversation_id = %s
                ORDER BY created_at ASC
                """,
                (conversation_id,),
            )
            return cur.fetchall()

    finally:
        conn.close()

def edit_direct_conversation_message(message_id, message_text):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE direct_messages
                SET content = %s, is_edited = TRUE, edited_at = NOW()
                WHERE id = %s
                """,
                (message_text, message_id),
            )

        conn.commit()
        return True

    finally:
        conn.close()

def get_direct_conversation_by_message_id(message_id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM direct_messages
                WHERE id = %s
                """,
                (message_id,),
            )
            return cur.fetchone()

    finally:
        conn.close()

def delete_message(message_id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM direct_messages
                WHERE id = %s
                """,
                (message_id,),
            )

        conn.commit()
        return True

    finally:
        conn.close()