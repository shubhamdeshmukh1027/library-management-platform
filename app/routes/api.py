from flask import Blueprint, jsonify, request

from app.services.library_service import (
    add_book,
    add_user,
    borrow_book,
    get_user,
    return_book,
    search_books,
)

api = Blueprint("api", __name__)


@api.get("/health")
def health():
    return jsonify({
        "status": "UP",
        "service": "Enterprise Smart Library Management Platform",
        "version": "1.0.0"
    })


@api.post("/users")
def create_user():
    data = request.get_json() or {}

    try:
        user = add_user(
            data.get("user_id"),
            data.get("name"),
            data.get("email"),
            data.get("role"),
        )
        return jsonify(user), 201

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@api.get("/users/<user_id>")
def fetch_user(user_id):
    try:
        return jsonify(get_user(user_id))

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404


@api.get("/books")
def list_books():
    query = request.args.get("q", "")
    return jsonify(search_books(query))


@api.post("/books")
def create_book():
    data = request.get_json() or {}

    try:
        book = add_book(
            data.get("book_id"),
            data.get("title"),
            data.get("author"),
            data.get("isbn"),
            data.get("total_copies", 0),
        )
        return jsonify(book), 201

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@api.post("/borrow")
def borrow():
    data = request.get_json() or {}

    try:
        loan = borrow_book(
            data.get("user_id"),
            data.get("book_id"),
        )
        return jsonify(loan), 201

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@api.post("/return")
def return_book_endpoint():
    data = request.get_json() or {}

    try:
        loan = return_book(data.get("loan_id"))
        return jsonify(loan)

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400