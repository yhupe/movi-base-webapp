from flask import Flask, render_template
from data.data_managers.sqlite_data_manager import SQLiteDataManager
from data.models.data_models import db, Movie
import os


app = Flask(__name__)

# db_path returns absolute path of current working directory with passed filename
db_name = 'movie_base.sqlite'
db_path = os.path.abspath(db_name)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db.init_app(app)

data_manager = SQLiteDataManager(db)

"""with app.app_context():
    db.create_all()"""


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"

@app.route('/users', methods=['GET'])
def list_users():
    users = data_manager.get_all_users()

    return render_template('users.html', users=users)

@app.route('/users/<user_id>', methods=['GET'])
def user_movies(user_id):

    return str(data_manager.get_user_movies(user_id))

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    pass

@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):

    statement = data_manager.add_user_movie(user_id, 'Inception')
    db.session.execute(statement)
    db.session.commit()
    return "movie added sucessfully!"

@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie():
    pass

@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['POST'])
def delete_movie():
    pass


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)