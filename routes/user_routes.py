from flask import request, jsonify
from services.user_service import (
    fetch_all_users, fetch_user_by_id, add_user,
    modify_user, remove_user, search_users_by_name,
    login_user
)

def register_routes(app):
    @app.route('/')
    def home():
        return "User Management System"

    @app.route('/users', methods=['GET'])
    def get_all_users():
        return fetch_all_users()

    @app.route('/user/<user_id>', methods=['GET'])
    def get_user(user_id):
        return fetch_user_by_id(user_id)

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        return add_user(data)

    @app.route('/user/<user_id>', methods=['PUT'])
    def update_user(user_id):
        data = request.get_json()
        return modify_user(user_id, data)

    @app.route('/user/<user_id>', methods=['DELETE'])
    def delete_user(user_id):
        return remove_user(user_id)

    @app.route('/search', methods=['GET'])
    def search_users():
        name = request.args.get('name')
        return search_users_by_name(name)

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        return login_user(data)
