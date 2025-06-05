#!/usr/bin/env python3
"""
Basic Flask App
This module sets up a simple Flask application with a single route.
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """Welcome message route
    
    Returns:
        JSON: A welcome message payload
    """
    return jsonify({"message": "Bienvenue"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
