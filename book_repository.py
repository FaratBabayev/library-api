from db import connect

def get_all_books(available_only=False):
    conn = connect()

    if available_only:
        rows = conn.execute(
            "SELECT * FROM books WHERE available = 1"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM books"
        ).fetchall()

    conn.close()
    return rows

def get_book_by_id(book_id):
    conn = connect()

    book = conn.execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id,)
    ).fetchone()

    conn.close()
    return book


def create_book(title, author, isbn):
    conn = connect()

    cursor = conn.execute(
        """
        INSERT INTO books (title, author, isbn, available)
        VALUES (?, ?, ?, 1)
        """,
        (title, author, isbn)
    )

    conn.commit()

    book = conn.execute(
        "SELECT * FROM books WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()

    conn.close()
    return book


def delete_book(book_id):
    conn = connect()

    conn.execute(
        "DELETE FROM books WHERE id = ?",
        (book_id,)
    )

    conn.commit()
    conn.close()