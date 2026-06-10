from core.database import get_connection

def create_group_conversation(group_name, description, creator_id):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO group_conversations
                (
                    name,
                    description,
                    created_by
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
                RETURNING *
                """,
                (group_name, description, creator_id),
            )
            conversation = cur.fetchone()

        conn.commit()
        return conversation

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


def get_group_conversation_by_group_and_creator(group_name, creator_id):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM group_conversations
                WHERE name = %s AND created_by = %s
                """,
                (group_name, creator_id),
            )
            return cur.fetchone()

    finally:
        conn.close()

def get_user_group(user_id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM group_conversations
                WHERE created_by = %s OR id IN (SELECT group_id FROM group_members WHERE user_id = %s)
                """,
                (user_id, user_id),
            )
            return cur.fetchall()

    finally:
        conn.close()

def add_user_to_group_conversation(group_id, user_id, role):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO group_members
                (
                    group_id,
                    user_id,
                    role
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
                RETURNING *
                """,
                (group_id, user_id, role),
            )
            membership = cur.fetchone()

        conn.commit()
        return membership

    finally:
        conn.close()

def get_group_conversation_by_id(group_id):

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

def get_group_by_id(group_id, user_id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM group_conversations
                WHERE id = %s AND (created_by = %s OR id IN (SELECT group_id FROM group_members WHERE user_id = %s))
                """,
                (group_id, user_id, user_id),
            )
            return cur.fetchone()

    finally:
        conn.close()

def update_group_conversation(group_id, user_id, new_group_name, new_description):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE group_conversations
                SET name = %s, description = %s
                WHERE id = %s AND id IN (SELECT group_id FROM group_members WHERE user_id = %s AND role = 'admin' AND group_id = %s)
                RETURNING *
                """,
                (new_group_name, new_description, group_id, user_id, group_id),
            )
            updated_conversation = cur.fetchone()

        conn.commit()
        return updated_conversation

    finally:
        conn.close()

def delete_group_conversation(group_id, user_id):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM group_conversations
                WHERE id = %s AND id IN (SELECT group_id FROM group_members WHERE user_id = %s AND role = 'admin' AND group_id = %s)
                RETURNING *
                """,
                (group_id, user_id, group_id),
            )
            deleted_conversation = cur.fetchone()

        conn.commit()
        return deleted_conversation

    finally:
        conn.close()