from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    """Abstract class serving as an abstraction layer to define
    the fundamental methods, which all inheriting data managers have to implement
    to create a uniform interface."""

    @abstractmethod
    def validate_movie_data(self, movie_data: dict) -> bool:
        pass

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def add_user(self, user_data):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_user_movie(self, movie_data):
        pass

    @abstractmethod
    def delete_user_movie(self, user_id):
        pass

    @abstractmethod
    def update_user_movie(self, movie_id, updated_movie_data):
        pass

# ideas: search_movie, filter_movies, random_movie, movie_stats, ...