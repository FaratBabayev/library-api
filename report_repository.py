from db import connect


def get_overdue_loans():
    conn = connect()

    rows = conn.execute(
        """
        SELECT loans.id, books.title, members.name, loans.due_date
        FROM loans
        JOIN books ON books.id = loans.book_id
        JOIN members ON members.id = loans.member_id
        WHERE loans.returned = 0
        """
    ).fetchall()

    conn.close()
    return rows


def get_report_summary_data():
    conn = connect()

    total_books = conn.execute(
        "SELECT COUNT(*) FROM books"
    ).fetchone()[0]

    loans = conn.execute(
        "SELECT * FROM loans"
    ).fetchall()

    conn.close()

    return total_books, loans