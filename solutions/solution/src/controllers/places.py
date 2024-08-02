"""
Places controller module
"""
from flask_jwt_extended import jwt_required
from flask import abort, request, Blueprint, render_template
from solutions.solution.src.models.place import Place
from solutions.solution.src.models.review import Review
from solutions.solution.src.models.country import Country


places_bp = Blueprint('places', __name__)


@places_bp.route('/', methods=['POST'])
def create_place():
    """Creates a new place"""
    data = request.get_json()
    try:
        place = Place.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(404, str(e))
    return place.to_dict(), 201


@places_bp.route('/', methods=['GET'])
def get_places():
    """Returns all places"""
    places: list[Place] = Place.get_all()
    return [place.to_dict() for place in places], 200
    

@places_bp.route('/<place_id>', methods=['GET'])
def get_place_by_id(place_id: str):
    """Returns a place by ID"""
    place: Place | None = Place.get(place_id)
    if not place:
        abort(404, f"Place with ID {place_id} not found")
    return place.to_dict(), 200


@places_bp.route('/<place_id>', methods=['PUT'])
def update_place(place_id: str):
    """Updates a place by ID"""
    data = request.get_json()
    try:
        place: Place | None = Place.update(place_id, data)
    except ValueError as e:
        abort(400, str(e))
    if not place:
        abort(404, f"Place with ID {place_id} not found")
    return place.to_dict(), 200

@places_bp.route('/<place_id>', methods=['DELETE'])
def delete_place(place_id: str):
    """Deletes a place by ID"""
    if not Place.delete(place_id):
        abort(404, f"Place with ID {place_id} not found")
    return "", 204


@places_bp.route('/<place_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(place_id: str):
    """Creates a new review"""
    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing field: user_id")
    if "comment" not in data:
        abort(400, "Missing field: comment")
    if "rating" not in data:
        abort(400, "Missing field: rating")
    try:
        review = Review.create(data | {"place_id": place_id})
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    return review.to_dict(), 201

@places_bp.route('/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id: str):
    """Returns all reviews from a specific place"""
    reviews = Review.get_all()
    return [
        review.to_dict() for review in reviews if review.place_id == place_id
    ], 200

@places_bp.route('/<code>', methods=['GET'])
def get_country_places(code: str):
    """Returns all places for a specific country"""
    country: Country | None = Country.get_by_code(code)
    if not country:
        abort(404, f"Country with ID {code} not found")
    places: list[Place] = Place.get_all()
    country_places = [
        place.to_dict() for place in places if place.country_code == country.code
    ]
    return country_places