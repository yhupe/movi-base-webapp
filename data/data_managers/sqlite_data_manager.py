from curses.ascii import isalpha

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, insert, select, update, insert
from .data_manager_interface import DataManagerInterface
from data.models.data_models import User, Movie, user_movies
import requests

api_key = "f86d81ee"

URL = f"https://www.omdbapi.com/?apikey={api_key}"


class SQLiteDataManager(DataManagerInterface):

    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all_users(self):
        users = self.db.session.query(User) \
            .all()

        return users

    def get_user_by_id(self, user_id):
        user = User.query.get(user_id)

        if user:
            return user
        else:
            return None

    def add_user(self, new_username):

        users = self.db.session.query(User) \
            .all()

        user_exists = any(user.username == new_username for user in users)

        if not user_exists:

            statement = insert(User).values(username=new_username)
            return statement

        else:
            return False



    def delete_user(self, user_id):
        pass

    def get_user_movies(self, user_id):
        user = User.query.get(user_id)

        if user:
            # Fetching movies through the relationship
            movies = user.movies
            return movies
        else:
            # if no user is found
            return None

    def get_movie_by_id(self, movie_id):
        movie = Movie.query.get(movie_id)

        return movie

    def fetch_new_movie(self, title):
        try:
            query_string = f"&t={title}"
            response = requests.get(URL + query_string)
            response_json = response.json()

            if response_json['Response'] == "True":

                if response.status_code == 200:

                    title = response_json["Title"]
                    year = response_json["Year"]
                    try:
                        imdb_rating = (
                            float(response_json["Ratings"][0]["Value"][:2]))

                    except IndexError:
                        imdb_rating = "N/A"

                    director = response_json["Director"]
                    genre = response_json["Genre"]
                    poster_link = response_json["Poster"]


                    movie = Movie(title= title, release_year=year, director=director, genre=genre, poster_link=poster_link)

                    self.db.session.add(movie)
                    self.db.session.commit()

                    return movie.movie_id

                else:
                    print(f"Error: API returned status code "
                          f"{response.status_code}")

            else:
                print(f"('{title}') --- {response_json['Error']}")

        except requests.exceptions.ConnectionError:
            print("Error: connection to OMDb API failed!")


    def add_user_movie(self, user_id, title):
        user = User.query.get(user_id)
        movie = Movie.query.filter(func.lower(Movie.title) \
                           .ilike(func.lower(f"%{title}%"))) \
                           .first()

        if user:
            if movie:
                movie_id = movie.movie_id
                print(f"Movie data for '{movie}' was found in the database.")

            elif not movie:
                movie_id = self.fetch_new_movie(title)
                print(f"Movie data for '{title}' was not found in the database."
                      f"Movie data is being fetched from OMDb API ... ")


            statement = insert(user_movies).values(user_id=user_id, movie_id=movie_id, rating=None)

            return statement

        else:
            print(user_id)
            print("User id not found!")
            return False


    def delete_user_movie(self, user_id, movie_id):
        user = User.query.get(user_id)
        movie = Movie.query.get(movie_id)

        if user and movie:
            if movie in user.movies:
                user.movies.remove(movie)
                return True
            else:
                return False
        else:
            return False

    def get_personal_details(self, user_id, movie_id):

        statement = select(user_movies.c.rating, user_movies.c.comment).where(
            (user_movies.c.user_id == user_id) & (user_movies.c.movie_id == movie_id)
        )

        return statement

    def update_user_movie(self, user_id, movie_id, update_values):

        statement = ""

        if user_id and movie_id:

            if 'rating' in update_values or 'comment' in update_values:
                statement = update(user_movies).where(
            (user_movies.c.user_id == user_id) & (user_movies.c.movie_id == movie_id)
            ).values(**update_values)

        if statement == "":
            return None

        else:
            return statement


    def get_movie_rating_and_comment(self, user_id):

        if user_id:

            statement = select(
        user_movies.c.movie_id,
        user_movies.c.rating,
        user_movies.c.comment
    ).where(user_movies.c.user_id == user_id)

            return statement

        else:
            return None