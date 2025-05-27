#!/usr/bin/env python3
"""
Main Flask app for the API.
"""

import os
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from api.v1.auth.auth import Auth

app = Flask(__name__)
app.register_blueprint(app_views)

# Initialize auth based on AUTH_TYPE environment variable
auth = None
auth_type = os.getenv('AUTH_TYPE', '')
if auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
else:
    auth = Auth()

@app.errorhandler(401)
def unauthorized(error) -> tuple:
    """
    Handle 401 Unauthorized errors.

    Returns:
        tuple: JSON error message and HTTP status code 401.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> tuple:
    """
    Handle 403 Forbidden errors.

    Returns:
        tuple: JSON error message and HTTP status code 403.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """
    Filter requests before processing to enforce authentication.
    Checks if the path requires authentication and validates the user.
    """
    if auth is None:
        return
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_paths):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


if __name__ == "__main__":
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', 5000))
    app.run(host=host, port=port)
