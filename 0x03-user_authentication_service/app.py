#!/usr/bin/emv python3
"""Flask app"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def root():
    """Root route for our app"""
    return jsonify({'message':'Bienvenue'})