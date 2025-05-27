#!/usr/bin/env python3
"""
Flask application module for the user data API.
Sets up the Flask app, error handlers, and request filtering.
"""

from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app)

# Initialize auth based on AUTH_TYPE environment variable
auth = None
if os.getenv('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()

@app.errorhandler(401)
def unauthorized(error):
    """
    Handle 401 Unauthorized errors.

    Args:
        error: The error object.

    Returns:
        JSON response with error message and 401 status code.
    """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error):
    """
    Handle 403 Forbidden errors.

    Args:
        error: The error object.

    Returns:
        JSON response with error message and 403 status code.
    """
    return jsonify({"error": "Forbidden"}), 403

@app.before_request
def before_request():
    """
    Filter requests before processing to enforce authentication.

    - Does nothing if auth is None.
    - Does nothing if the request path is in ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/'].
    - Aborts with 401 if auth.authorization_header(request) returns None.
    - Aborts with 403 if auth.current_user(request) returns None.
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
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 5000))
    app.run(host=host, port=port)
