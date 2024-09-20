"""
Front_end controller module
"""

from flask import abort, request, Blueprint, render_template, redirect, url_for
from solutions.solution.src.models.place import Place
from solutions.solution.src.models.review import Review


home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home_places():
    return render_template('index.html')

@home_bp.route('/place')
def home_place():
    return render_template('place.html')

@home_bp.route('/login')
def home_login():
    return render_template('login.html')

@home_bp.route('/add_review')
def home_add_review():
    return render_template('add_review.html')
