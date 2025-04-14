from crypt import methods

from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy.testing.suite.test_reflection import users

from data.data_managers.sqlite_data_manager import SQLiteDataManager
from data.models.data_models import db, Movie, User
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


@app.route('/', methods=['GET'])
def home():
    users = data_manager.get_all_users()

    return render_template('index.html', users=users)

@app.route('/users', methods=['GET'])
def list_users():
    # kind of redundant because all existing users are visible in the dropdown menu
    users = data_manager.get_all_users()

    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):

    username = data_manager.get_user_by_id(user_id)
    user_movie_data = data_manager.get_user_movies(user_id)
    users = data_manager.get_all_users()
    added_message = request.args.get('added')

    return render_template('movies.html', movies=user_movie_data, user=username, user_id=user_id, all_users=users, added_message=added_message), 200

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():

    if request.method == "GET":
        return render_template('add_user.html'), 200

    if request.method == "POST":
        new_username = request.form.get('username')

        if not new_username:
            return "Please enter a new username", 400

        statement = data_manager.add_user(new_username)

        if statement is not False:
            db.session.execute(statement)
            db.session.commit()
            print(f"New user profile added for '{new_username}'.")
            user = User.query.filter_by(username=new_username).first()

            return jsonify({'user_id': user.user_id}), 201

        else:
            print(f"username '{new_username}' exists already.")
            return (f"username '{new_username}' exists already. \n"
                    f"You will be redirected to the account management page."), 409

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):

    if request.method == "GET":
        return render_template('add_movie.html', user_id=user_id), 200

    if request.method == "POST":

        user = User.query.get(user_id)
        title = request.form.get('title')

        statement = data_manager.add_user_movie(user_id, title)
        db.session.execute(statement)
        db.session.commit()

        print(f"movie {title} added successfully to user profile '{user.username}'(id {user.user_id})")
        return redirect(url_for('user_movies', user_id=user_id, added=True)), 200

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    # adding an a-tag (class="action-button" or similar to delete-button)
    # with href to the update_movie.html form
    # action must be the url of this endpoint
    #

    user = data_manager.get_user_by_id(user_id)
    movie = data_manager.get_movie_title(movie_id)
    user_movie_data = None



    if request.method == "GET":

        statement = data_manager.get_personal_details(user_id, movie_id)

        result = db.session.execute(statement).fetchone()

        if result:
            user_movie_data = {'rating': result.rating} #, 'comment': result.comment

        return render_template('update_movie.html', user=user, movie=movie, user_movie=user_movie_data)

    if request.method == "POST":
        # add own personal rating
        # add personal comments on the movie
        # green/ red success or fail message after submitting form
        # and redirecting back to user_movies endpoint
        pass

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):

    username = data_manager.get_user_by_id(user_id)
    movie = data_manager.get_movie_title(movie_id)

    if user_id and movie_id:
        data_manager.delete_user_movie(user_id, movie_id)
        db.session.commit()
        print(f"'{movie.title}' deleted from {username}'s profile")

        return redirect(url_for('user_movies', user_id=user_id)), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)