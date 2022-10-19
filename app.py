# app.py
from flask import request
from flask_restx import Resource, Api

from config import app, db
from models import Movie, Director, Genre
from schemas import MovieSchema, DirectorSchema, GenreSchema

api = Api(app)

# создаем namespace
movies_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@movies_ns.route("/")
class MovieView(Resource):
    def get(self):
        query = Movie.query

        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        page = request.args.get('page')  # запрос параметра номера страницы

        if director_id:
            query = query.filter(Movie.director_id == director_id)  # + where director_id = director_id

        if genre_id:
            query = query.filter(Movie.genre_id == genre_id)  # + and

        # if genre_id:= request.args.get('genre_id')  - работает в Python 3.10

        if page:
            query = query.paginate(int(page), 2).items

        return movies_schema.dump(query), 200

    def post(self):
        data = request.json
        try:
            db.session.add(
                Movie(
                    **data
                )
            )
            db.session.commit()
            return "Данные добавлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 405


@movies_ns.route("/<int:mid>")
class MovieView(Resource):
    def get(self, mid):
        try:
            query = Movie.query.get(mid)
            return movie_schema.dump(query), 200
        except Exception as e:
            print(e)
            return e, 404

    def put(self, mid):
        data = request.json

        try:
            # Movie.update().values(data).where(Movie.id == mid) - ещё один способ обновления
            db.session.query(Movie).filter(Movie.id == mid).update(
                data
            )
            db.session.commit()
            return "Данные обновлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 404

    def delete(self, mid):
        data = request.json
        try:
            db.session.query(Movie).filter(Movie.id == mid).delete()
            db.session.commit()
            return "Данные удалены", 204
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 404


@director_ns.route("/")
class DirectorView(Resource):
    def get(self):
        query = Director.query

        page = request.args.get('page')  # запрос параметра номера страницы

        if page:
            query = query.paginate(int(page), 2).items

        return directors_schema.dump(query), 200

    def post(self):
        data = request.json
        try:
            db.session.add(
                Director(
                    **data
                )
            )
            db.session.commit()
            return "Данные добавлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 405


@director_ns.route("/<int:did>")
class DirectorView(Resource):
    def get(self, did):
        try:
            query = Director.query.get(did)
            return director_schema.dump(query), 200

        except Exception as e:
            print(e)
            return e, 404

    def put(self, did):
        data = request.json

        try:
            db.session.query(Director).filter(Director.id == did).update(
                data
            )
            db.session.commit()
            return "Данные обновлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 404

    def delete(self, did):
        data = request.json
        try:
            db.session.query(Director).filter(Director.id == did).delete()
            db.session.commit()
            return "Данные удалены", 204
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 404


@genre_ns.route("/")
class GenreView(Resource):
    def get(self):
        query = Genre.query

        page = request.args.get('page')  # запрос параметра номера страницы

        if page:
            query = query.paginate(int(page), 2).items

        return genres_schema.dump(query), 200

    def post(self):
        data = request.json
        try:
            db.session.add(
                Genre(
                    **data
                )
            )
            db.session.commit()
            return "Данные добавлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 405


@genre_ns.route("/<int:gid>")
class GenreView(Resource):
    def get(self, gid):
        try:
            query = Genre.query.get(gid)
            return genre_schema.dump(query), 200
        except Exception as e:
            print(e)
            return e, 404

    def put(self, gid):
        data = request.json

        try:
            db.session.query(Genre).filter(Genre.id == gid).update(
                data
            )
            db.session.commit()
            return "Данные обновлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 404

    def delete(self, gid):
        data = request.json
        try:
            db.session.query(Genre).filter(Genre.id == gid).delete()
            db.session.commit()
            return "Данные удалены", 204
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 404


if __name__ == '__main__':
    app.run(debug=True)
