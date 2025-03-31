from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Table

db = SQLAlchemy()

"""user_movies is a linking table to link movie_id's to user_id's
to avoid repeating movie information, for example:
user_1 and user_2 both save the same movie to their account,
would mean to have double records with only varying foreign key user_id and 
different personal rating"""

user_movies = Table('user_movies', db.metadata,
        Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
        Column('movie_id', Integer, ForeignKey('movies.movie_id'), primary_key=True),
        Column('rating', String)
)


class Movie(db.Model):

    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    release_year = Column(Integer)
    director = Column(String)
    genre = Column(String)

    def __repr__(self):
        return f"Movie: {self.title} - Genre: {self.genre})"

class User(db.Model):

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    movies = db.relationship('Movie', secondary=user_movies, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"User: {self.username} - ID: {self.user_id})"