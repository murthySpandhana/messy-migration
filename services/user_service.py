from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from db import get_db
from utils.validators import is_valid_email

def fetch_all_users():
    try:
        conn, cursor = get_db()
        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()
        result = [{"id": u[0], "name": u[1], "email": u[2]} for u in users]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def fetch_user_by_id(user_id):
    try:
        conn, cursor = get_db()
        cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            return jsonify({"id": user[0], "name": user[1], "email": user[2]}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def add_user(data):
    try:
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not all([name, email, password]):
            return jsonify({"error": "Missing required fields"}), 400

        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        hashed_password = generate_password_hash(password)
        conn, cursor = get_db()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                       (name, email, hashed_password))
        conn.commit()
        return jsonify({"message": "User created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def modify_user(user_id, data):
    try:
        name = data.get("name")
        email = data.get("email")

        if not all([name, email]):
            return jsonify({"error": "Name and email required"}), 400

        conn, cursor = get_db()
        cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?",
                       (name, email, user_id))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": "User updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def remove_user(user_id):
    try:
        conn, cursor = get_db()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": f"User {user_id} deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def search_users_by_name(name):
    try:
        if not name:
            return jsonify({"error": "Please provide a name to search"}), 400

        conn, cursor = get_db()
        cursor.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",))
        users = cursor.fetchall()
        result = [{"id": u[0], "name": u[1], "email": u[2]} for u in users]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def login_user(data):
    try:
        email = data.get("email")
        password = data.get("password")

        if not all([email, password]):
            return jsonify({"error": "Email and password required"}), 400

        conn, cursor = get_db()
        cursor.execute("SELECT id, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[1], password):
            return jsonify({"status": "success", "user_id": user[0]}), 200
        else:
            return jsonify({"status": "failed"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
