#!/usr/bin/env python3
"""
Index views for the API.
Provides status, unauthorized, and forbidden endpoints.
"""

from flask import Blueprint, jsonify, abort

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

@app_views.route('/status', methods=['GET'])
def status():
    """
    Return the status of the API.

    Returns:
        JSON response with status "OK".
    """
    return jsonify({"status": "OK"})

@app_views.route('/unauthorized', methods=['GET'])
def unauthorized():
    """
    Raise a 401 Unauthorized error.

    Returns:
        None: Always aborts with a 401 status code.
    """
    abort(401)

@app_views.route('/forbidden', methods=['GET'])
def forbidden():
    """
    Raise a 403 Forbidden error.

    Returns:
        None: Always aborts with a 403 status code.
    """
    abort(403)
