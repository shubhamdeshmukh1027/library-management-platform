import pytest

from database.db import db
from app.services.library_service import (
    add_user,
    borrow_book,
    delete_user,
)


@pytest.fixture(autouse=True)
def reset_database():
    db.reset()
    yield
    db.reset()


def test_add_user_success():
    user = add_user(
        "U103",
        "John Doe",
        "john.doe@university.edu",
        "Student",
    )

    assert user["user_id"] == "U103"
    assert user["name"] == "John Doe"
    assert user["role"] == "Student"


def test_duplicate_user_raises():
    add_user(
        "U103",
        "John Doe",
        "john.doe@university.edu",
        "Student",
    )

    with pytest.raises(ValueError):
        add_user(
            "U103",
            "Another User",
            "another@university.edu",
            "Student",
        )


def test_delete_user_with_active_loan_fails():
    add_user(
        "U103",
        "John Doe",
        "john.doe@university.edu",
        "Student",
    )

    borrow_book("U103", "B001")

    with pytest.raises(ValueError):
        delete_user("U103")