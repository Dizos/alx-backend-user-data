#!/usr/bin/env python3
"""
Basic Flask App with User Registration
This module sets up a Flask application with user registration endpoint.
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()

@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """Welcome message route
    
    Returns:
        JSON: A welcome message payload
    """
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """Register a new user
    
    Returns:
        JSON: Registration status message
    """
    # Get form data
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Validate input
    if not email or not password:
        return jsonify({"message": "email and password required"}), 400
    
    try:
        # Attempt to register the user
        user = AUTH.register_user(email, password)
        return jsonify({
            "email": user.email,
            "message": "user created"
        })
    except ValueError:
        # Handle case where user already exists
        return jsonify({
            "message": "email already registered"
        }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
