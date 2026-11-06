from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from sqlalchemy import select
from email_validator import validate_email, EmailNotValidError

from app import db
from app.models import User

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = data.get("password", "")

    if not name or len(name) > 100:
        return jsonify({"error": "Enter a valid name"}), 400

    if not isinstance(password, str) or len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError:
        return jsonify({"error": "Enter a valid email address"}), 400

    existing = db.session.scalar(
        select(User).where(User.email == email)
    )

    if existing:
        return jsonify({"error": "Email already registered"}), 409

    user = User(name=name, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Registration successful",
        "user_id": user.id
    }), 201


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = str(data.get("email", "")).strip().lower()
    password = data.get("password", "")

    user = db.session.scalar(
        select(User).where(User.email == email)
    )

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    login_user(user)

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    })


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"})
