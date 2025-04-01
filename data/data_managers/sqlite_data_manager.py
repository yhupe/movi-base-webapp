from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert
from .data_manager_interface import DataManagerInterface
from data.models.data_models import User, Movie, user_movies
import requests

api_key = "f86d81ee"

URL = f"https://www.omdbapi.com/?apikey={api_key}"


class SQLiteDataManager(DataManagerInterface):

    def __init__(self, db: SQLAlchemy):
        self.db = db

    def validate_movie_data(self, movie_data: dict) -> bool:
        pass

    def get_all_users(self):
        users = self.db.session.query(User) \
            .all()

        return users

    def add_user(self, user_data):
        pass

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
                    print(f"Movie {title} (id: {movie.movie_id}) added successfully.")

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
        movie = Movie.query.filter_by(title=title).first()

        if user:
            if user and movie:
                movie_id = movie.movie_id

            elif user and not movie:
                movie_id = self.fetch_new_movie(title)



            statement = insert(user_movies).values(user_id=user_id, movie_id=movie_id, rating=None)

            return statement

        else:
            print("User id not found!")
            return False


    def delete_user_movie(self, user_id, movie_id):
        pass

    def update_user_movie(self, user_id, movie_id, updated_movie_data):
        pass
