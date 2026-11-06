
from db import connect


def get_all_loans():
    conn = connect()

    rows = conn.execute(
        "SELECT * FROM loans"
    ).fetchall()

    conn.close()
    return rows


def get_loan_by_id(loan_id):
    conn = connect()

    loan = conn.execute(
        "SELECT * FROM loans WHERE id = ?",
        (loan_id,)
    ).fetchone()

    conn.close()
    return loan


def get_loans_by_member(member_id):
    conn = connect()

    rows = conn.execute(
        "SELECT * FROM loans WHERE member_id = ?",
        (member_id,)
    ).fetchall()

    conn.close()
    return rows

def create_loan_record(book_id, member_id, due_date, checked_out):
    conn = connect()

    cursor = conn.execute(
        """
        INSERT INTO loans (book_id, member_id, due_date, checked_out)
        VALUES (?, ?, ?, ?)
        """,
        (book_id, member_id, due_date, checked_out)
    )

    conn.execute(
        "UPDATE books SET available = 0 WHERE id = ?",
        (book_id,)
    )

    conn.commit()

    loan = conn.execute(
        "SELECT * FROM loans WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()

    conn.close()
    return loan