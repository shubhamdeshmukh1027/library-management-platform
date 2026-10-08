import pytest

from database.db import db
from app.services.library_service import (
    add_user,
    borrow_book,
    return_book,
)


@pytest.fixture(autouse=True)
def reset_database():
    db.reset()
    yield
    db.reset()


def test_borrow_and_return_lifecycle():
    loan = borrow_book("U101", "B001")

    assert loan["status"] == "ACTIVE"
    assert db.books["B001"]["available_copies"] == 4
    assert db.users["U101"]["active_loans"] == 1

    returned = return_book(loan["loan_id"])

    assert returned["status"] == "RETURNED"
    assert db.books["B001"]["available_copies"] == 5
    assert db.users["U101"]["active_loans"] == 0


def test_student_loan_quota():
    add_user(
        "U103",
        "John Doe",
        "john.doe@university.edu",
        "Student",
    )

    borrow_book("U103", "B001")
    borrow_book("U103", "B002")
    borrow_book("U103", "B001")

    with pytest.raises(ValueError):
        borrow_book("U103", "B002")