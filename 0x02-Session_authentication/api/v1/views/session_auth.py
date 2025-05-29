#!/usr/bin/env python3
"""
Session authentication routes for the API.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from os import getenv

@app_views.route('/auth_session/login', '/auth_session/login/', methods=['POST'], strict_slashes=False)
def login():
    """
    Handles user login and creates a session.

    Retrieves email and password from form data, validates the user, and creates a session ID.
    Sets the session ID as a cookie and returns the user's JSON representation.

    Returns:
        JSON: User data on successful login, or error message with appropriate status code.
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]  # Assume the first user if multiple are found
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response

@app_views.route('/auth_session/logout', '/auth_session/logout/', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Handles user logout by destroying the session.

    Deletes the session ID from the session store using the session cookie.

    Returns:
        JSON: Empty dictionary on success, or aborts with 404 if session deletion fails.
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
