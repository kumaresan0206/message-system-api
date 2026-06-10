from core.database import get_connection

def add_user_to_group_conversation(group_id, user_id):

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
                    'member'
                )
                """,
                (group_id, user_id),
            )

        conn.commit()

    finally:
        conn.close()

def get_group_conversation_members(group_id):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM group_members
                WHERE group_id = %s
                """,
                (group_id,),
            )
            return cur.fetchall()

    finally:
        conn.close()

def get_user_group(group_id, user_id):

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

def get_user_role_in_group(group_id, user_id):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT role
                FROM group_members
                WHERE group_id = %s AND user_id = %s
                """,
                (group_id, user_id),
            )
            result = cur.fetchone()
            return result[0] if result else None

    finally:
        conn.close()

def promote_member_to_admin(group_id, target_user_id):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE group_members
                SET role = 'admin'
                WHERE group_id = %s
                AND user_id = %s
                RETURNING *
                """,
                (group_id, target_user_id),
            )

            response = cur.fetchone()

        conn.commit()

        return response

    finally:
        conn.close()

def delete_member_from_group(group_id, target_user_id):

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM group_members
                WHERE group_id = %s AND user_id = %s
                """,
                (group_id, target_user_id),
            )

        conn.commit()

    finally:
        conn.close()