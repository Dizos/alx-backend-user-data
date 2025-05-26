#!/usr/bin/env python3
"""
Flask application module for the user data API.
Sets up the Flask app and error handlers.
"""

from flask import Flask, jsonify
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

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


if __name__ == "__main__":
    import os
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 5000))
    app.run(host=host, port=port)
