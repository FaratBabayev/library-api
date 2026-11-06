from db import connect
def get_all_members():
    conn = connect()
    rows = conn.execute(
        "SELECT * FROM members"
    ).fetchall()
    conn.close()
    return rows
def get_member_by_id(member_id):
    conn = connect()
    member = conn.execute(
        "SELECT * FROM members WHERE id = ?",
        (member_id,)
    ).fetchone()
    conn.close()
    return member
def get_member_by_email(email):
    conn = connect()
    member = conn.execute(
        "SELECT * FROM members WHERE email = ?",
        (email,)
    ).fetchone()
    conn.close()
    return member
def create_member(name, email, member_type):
    conn = connect()
    cursor = conn.execute(
        """
        INSERT INTO members (name, email, type)
        VALUES (?, ?, ?)
        """,
        (name, email, member_type)
    )
    conn.commit()
    member = conn.execute(
        "SELECT * FROM members WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()
    conn.close()
    return member