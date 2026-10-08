from database.db import db
from datetime import datetime


def add_user(user_id, name, email, role):
    if not user_id or not name or not email or not role:
        raise ValueError("All user fields are required")

    if user_id in db.users:
        raise ValueError("User already exists")

    if role not in ["Student", "Faculty"]:
        raise ValueError("Role must be Student or Faculty")

    db.users[user_id] = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "role": role,
        "active_loans": 0,
    }

    return db.users[user_id]


def get_user(user_id):
    if user_id not in db.users:
        raise ValueError("User not found")

    return db.users[user_id]


def delete_user(user_id):
    user = get_user(user_id)

    if user["active_loans"] > 0:
        raise ValueError("Cannot delete user with active loans")

    del db.users[user_id]

    return {"message": "User deleted successfully"}


def add_book(book_id, title, author, isbn, total_copies):
    if not book_id or not title or not author or not isbn:
        raise ValueError("All book fields are required")

    if book_id in db.books:
        raise ValueError("Book already exists")

    if total_copies <= 0:
        raise ValueError("Total copies must be greater than zero")

    db.books[book_id] = {
        "book_id": book_id,
        "title": title,
        "author": author,
        "isbn": isbn,
        "total_copies": total_copies,
        "available_copies": total_copies,
    }

    return db.books[book_id]


def get_book(book_id):
    if book_id not in db.books:
        raise ValueError("Book not found")

    return db.books[book_id]


def search_books(query=""):
    query = query.lower()

    results = []

    for book in db.books.values():
        if (
            query in book["title"].lower()
            or query in book["author"].lower()
            or query in book["isbn"].lower()
        ):
            results.append(book)

    return results


def borrow_book(user_id, book_id):
    user = get_user(user_id)
    book = get_book(book_id)

    if book["available_copies"] <= 0:
        raise ValueError("No available copies")

    max_books = 3 if user["role"] == "Student" else 5

    if user["active_loans"] >= max_books:
        raise ValueError("Loan limit exceeded")

    book["available_copies"] -= 1
    user["active_loans"] += 1

    loan = {
        "loan_id": f"L-{len(db.loans) + 1:04d}",
        "user_id": user_id,
        "book_id": book_id,
        "borrowed_at": datetime.utcnow().isoformat(),
        "status": "ACTIVE",
    }

    db.loans.append(loan)

    return loan


def return_book(loan_id):
    loan = next(
        (loan for loan in db.loans if loan["loan_id"] == loan_id),
        None
    )

    if not loan:
        raise ValueError("Loan not found")

    if loan["status"] == "RETURNED":
        raise ValueError("Book already returned")

    user = get_user(loan["user_id"])
    book = get_book(loan["book_id"])

    loan["status"] = "RETURNED"
    loan["returned_at"] = datetime.utcnow().isoformat()

    book["available_copies"] += 1
    user["active_loans"] -= 1

    return loan