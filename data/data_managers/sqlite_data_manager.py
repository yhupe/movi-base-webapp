from flask_sqlalchemy import SQLAlchemy
from .data_manager_interface import DataManagerInterface
from data.models.data_models import User, Movie


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
        pass

    def add_user_movie(self, movie_data):
        pass

    def delete_user_movie(self, user_id):
        pass

    def update_user_movie(self, movie_id, updated_movie_data):
        pass
