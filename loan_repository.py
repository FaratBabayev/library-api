
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

def return_loan_record(loan_id, fine):
    conn = connect()

    loan = conn.execute(
        "SELECT * FROM loans WHERE id = ?",
        (loan_id,)
    ).fetchone()

    if loan is None:
        conn.close()
        return None

    conn.execute(
        "UPDATE loans SET returned = 1, fine = ? WHERE id = ?",
        (fine, loan_id)
    )

    conn.execute(
        "UPDATE books SET available = 1 WHERE id = ?",
        (loan[1],)
    )

    conn.commit()

    member = conn.execute(
        "SELECT * FROM members WHERE id = ?",
        (loan[2],)
    ).fetchone()

    book = conn.execute(
        "SELECT * FROM books WHERE id = ?",
        (loan[1],)
    ).fetchone()

    updated = conn.execute(
        "SELECT * FROM loans WHERE id = ?",
        (loan_id,)
    ).fetchone()

    conn.close()

    return loan, member, book, updated

def renew_loan_record(loan_id, new_due):
    conn = connect()

    loan = conn.execute(
        "SELECT * FROM loans WHERE id = ?",
        (loan_id,)
    ).fetchone()

    if loan is None:
        conn.close()
        return None

    conn.execute(
        """
        UPDATE loans
        SET due_date = ?, renewals = renewals + 1
        WHERE id = ?
        """,
        (new_due, loan_id)
    )

    conn.commit()

    member = conn.execute(
        "SELECT * FROM members WHERE id = ?",
        (loan[2],)
    ).fetchone()

    book = conn.execute(
        "SELECT * FROM books WHERE id = ?",
        (loan[1],)
    ).fetchone()

    updated = conn.execute(
        "SELECT * FROM loans WHERE id = ?",
        (loan_id,)
    ).fetchone()

    conn.close()

    return member, book, updated
def pay_fine_record(loan_id):
    conn = connect()

    loan = conn.execute(
        "SELECT * FROM loans WHERE id = ?",
        (loan_id,)
    ).fetchone()

    if loan is None:
        conn.close()
        return None

    conn.execute(
        "UPDATE loans SET fine_paid = 1 WHERE id = ?",
        (loan_id,)
    )

    conn.commit()

    member = conn.execute(
        "SELECT * FROM members WHERE id = ?",
        (loan[2],)
    ).fetchone()

    updated = conn.execute(
        "SELECT * FROM loans WHERE id = ?",
        (loan_id,)
    ).fetchone()

    conn.close()

    return loan, member, updated