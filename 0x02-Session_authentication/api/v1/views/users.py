#!/usr/bin/env python3
"""
User-related API routes.
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from models import storage

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects.

    Returns:
        JSON list of all users.
    """
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a new User object.

    Returns:
        JSON representation of the new user or error message.
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object by ID or the authenticated user if user_id is 'me'.

    Args:
        user_id (str): The ID of the user or 'me' for the authenticated user.

    Returns:
        JSON representation of the user or error message.
    """
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_dict())
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object.

    Args:
        user_id (str): The ID of the user to update.

    Returns:
        JSON representation of the updated user or error message.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        Empty JSON response or error message.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200
