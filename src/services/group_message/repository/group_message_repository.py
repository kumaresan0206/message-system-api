from common.database.database import get_connection


def send_message_to_group(group_id, sender_id, message):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO group_messages
                (
                    group_conversation_id,
                    sender_id,
                    content
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
                RETURNING *
                """,
                (group_id, sender_id, message),
            )

            response = cur.fetchone()

        conn.commit()
        return response

    finally:
        conn.close()


def get_group_member(group_id, user_id):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM group_members
                WHERE group_id = %s AND user_id = %s
                """,
                (group_id, user_id),
            )
            return cur.fetchone()

    finally:
        conn.close()


def get_group(group_id):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM group_conversations
                WHERE id = %s
                """,
                (group_id,),
            )
            return cur.fetchone()

    finally:
        conn.close()


def get_group_messages(group_id):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM group_messages
                WHERE group_conversation_id = %s
                ORDER BY created_at DESC
                """,
                (group_id,),
            )
            return cur.fetchall()

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


def edit_group_message(message_id, sender_id, new_message):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE group_messages
                SET content = %s, is_edited = TRUE, edited_at = NOW()
                WHERE id = %s AND sender_id = %s
                RETURNING *
                """,
                (new_message, message_id, sender_id),
            )

            response = cur.fetchone()

        conn.commit()
        return response

    finally:
        conn.close()


def delete_group_message(message_id, sender_id):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM group_messages
                WHERE id = %s AND sender_id = %s
                RETURNING *
                """,
                (message_id, sender_id),
            )

            response = cur.fetchone()

        conn.commit()
        return response

    finally:
        conn.close()


def get_message_by_id(message_id):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM group_messages
                WHERE id = %s
                """,
                (message_id,),
            )
            return cur.fetchone()

    finally:
        conn.close()


def group_message_mark_as_read(message_id, user_id):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO group_message_reads
                (
                    message_id,
                    user_id
                )
                VALUES
                (
                    %s,
                    %s
                )
                ON CONFLICT (message_id, user_id) DO NOTHING
                RETURNING *
                """,
                (message_id, user_id),
            )

            response = cur.fetchone()

        conn.commit()
        return response

    finally:
        conn.close()
