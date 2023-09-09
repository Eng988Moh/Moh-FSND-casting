import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth.auth import AuthError, requires_auth
from database.models import Actor, Movie, db_drop_and_create_all, setup_db

ITEMS_PER_PAGE = 8

# This function takes a request object and a selection of items,
# and returns a paginated subset of the items based on the requested page number.


def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    list = [item.format() for item in selection]
    current_page = list[start:end]
    return current_page


def create_app(db_uri="", test_config=None):
    app = Flask(__name__)
    CORS(app)
    if db_uri:
        setup_db(app, db_uri)
    else:
        setup_db(app)

    # Uncomment these to reset the database

    with app.app_context():
        db_drop_and_create_all()

    @app.route('/Itsworking')
    def healthy():
        return jsonify({
            "Its working fine": True
        })

    @app.route('/actors', methods=['GET'])
    # @requires_auth('get:actors')
    def get_actors(jwt):
        actors = Actor.query.order_by(Actor.id).all()
        current_page, current_actors = paginate(request, actors)

        if len(current_actors) == 0:
            abort(404)

        try:
            return jsonify({
                "success": True,
                "actors": current_actors,
                "total_actors": len(actors),
                "current_page": current_page
            })
        except:
            abort(500)

    @app.route('/movies', methods=['GET'])
    # @requires_auth('get:movies')
    def get_movies(jwt):
        movies = Movie.query.order_by(Movie.id).all()
        current_page, current_movies = paginate(request, movies)

        if len(current_movies) == 0:
            abort(404)

        try:
            return jsonify({
                "success": True,
                "movies": current_movies,
                "total_movies": len(movies),
                "current_page": current_page
            })
        except:
            abort(500)

    @app.route('/actors', methods=['POST'])
    # @requires_auth('post:actors')
    def add_actor(jwt):
        body = request.get_json()

        try:
            name = body['name']
            age = body['age']
            gender = body['gender']

            if name is None or age is None or gender is None:
                return jsonify({
                    "success": False,
                    "error": "Missing field. Please provide all required fields."
                })

            new_actor = Actor(name=name, age=age, gender=gender)
            new_actor.insert()

            return jsonify({
                "success": True,
                "added": True,
                "total_actors": len(Actor.query.all())
            })
        except KeyError:
            abort(422)

    @app.route('/movies', methods=['POST'])
    # @requires_auth('post:movies')
    def add_movie(jwt):
        body = request.get_json()
        try:
            title = body['title']
            release_date = body['release_date']

            if title is None or release_date is None:
                return jsonify({
                    "success": False,
                    "error": "Missing field. Please provide all required fields."
                })

            new_movie = Movie(title=title, release_date=release_date)
            new_movie.insert()

            return jsonify({
                "success": True,
                "added": True,
                "total_movies": len(Movie.query.all())
            })
        except KeyError:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    # @requires_auth('patch:actors')
    def update_actor(jwt, id):
        body = request.get_json()
        try:
            name = body['name']
            age = body['age']
            gender = body['gender']

            if name is None or age is None or gender is None:
                return jsonify({
                    "success": False,
                    "error": "Missing field. Please provide all required fields."
                })

            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if actor is None:
                return jsonify({
                    "success": False,
                    "error": "Actor not found"
                })

            actor.update(name, age, gender)

        except:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    # @requires_auth('patch:movies')
    def update_movie(jwt, id):
        body = request.get_json()
        try:
            title = body['title']
            release_date = body['release_date']

            if title is None or release_date is None:
                return jsonify({
                    "success": False,
                    "error": "Missing field. Please provide all required fields."
                })

            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie is None:
                return jsonify({
                    "success": False,
                    "error": "Movie not found"
                })

            movie.update(title, release_date)

        except:
            abort(422)

    @ app.route('/actors/<int:id>', methods=['DELETE'])
    # @requires_auth('delete:actors')
    def delete_actor(jwt, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            return jsonify({
                "success": False,
                "error": "Actor not found"
            }), 404

        try:
            actor.delete()
            return jsonify({
                "success": True,
                "deleted": True,
                "total_actors": len(Actor.query.all())
            })
        except:
            abort(422)

    @ app.route('/movies/<int:id>', methods=['DELETE'])
    # @requires_auth('delete:movies')
    def delete_movie(jwt, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            return jsonify({
                "success": False,
                "error": "Movie not found"
            }), 404

        try:
            movie.delete()
            return jsonify({
                "success": True,
                "deleted": True,
                "total_movies": len(Movie.query.all())
            })
        except:
            abort(422)


# Error Handling


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
