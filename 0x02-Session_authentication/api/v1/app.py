#!/usr/bin/env python3
"""
Flask application for the API with authentication.
"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from os import getenv
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)

auth = None
if getenv("AUTH_TYPE") == "basic_auth":
    auth = BasicAuth()
elif getenv("AUTH_TYPE") == "session_auth":
    auth = SessionAuth()

@app.before_request
def before_request():
    """
    Executes before each request to set up authentication.
    Assigns the authenticated user to request.current_user.
    """
    if auth is None:
        return
    excluded_paths = ['/api/v1/status', '/api/v1/auth_session/login/']
    if request.path in excluded_paths:
        return
    if not auth.require_auth(request.path, excluded_paths):
        return
    if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)
    request.current_user = auth.current_user(request)

@app.errorhandler(401)
def unauthorized(error):
    """
    Handles 401 Unauthorized errors.

    Returns:
        JSON response with error message and 401 status code.
    """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error):
    """
    Handles 403 Forbidden errors.

    Returns:
        JSON response with error message and 403 status code.
    """
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = int(getenv("API_PORT", 5000))
    app.run(host=host, port=port)
