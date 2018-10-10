"""Models and database functions for Epic StoryTime project."""

from flask_sqlalchemy import SQLAlchemy

#Connection to PostgreSQL database using Flask-SQLAlchemy helper library.
db = SQLAlchemy()

#Model definitions: database information.


class User(db.Model):
    """User of Epic StoryTime website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(64), nullable=True)
    lname = db.Column(db.String(64), nullable=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
#Q 1: Add a user image to the table (profile picture)
    # user_image = db.Column(db.)


    def __repr__(self):
        """Provide helpful representatble when printed."""

        return f"<user_id: {self.user_id} \n full_name = {self.fname} {self.lname} \n username: {self.username} \n email: {self.email} \n password: {self.password}>"


class GameMaster(db.Model):
    """Game Master of game(s)."""

    __tablename__ = "game_masters"

    gm_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    created_games = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=True)

    #Define relationship to User
    # user = db.relationship("User", 
    #                         backref=db.backref("users"))

    #Define relationship to Games
    # game = db.relationship("Game",
    #                         backref=db.backref("games"))

    def __repr__(self):
        return f"<gm_id: {gm_id} \n user_id: {user_id} \n created_games: {created_games}>"


class Player(db.Model):
    """Player of game(s)"""

    __tablename__ = "players"

    player_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    games_played = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=True)
    games_not_played = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=True)

    #Define relationship to User
    # user = db.relationship("User", 
    #                         backref=db.backref("users"))

    #Define relationship to Games
    # game = db.relationship("Game",
    #                         backref=db.backref("games"))

    def __repr__(self):
        return f"<player_id: {player_id} \n user_id: {user_id} \n games_played: {created_games} \n games_not_played: {games_not_played}>"


class Game(db.Model):
    """Game created by GM for Player"""

    __tablename__ = "games"

    game_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    game_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"<game_id: {game_id} \n game_name: {game_name} \n game_gm: {game_gm}>"


class GameInfo(db.Model):
    """Game point for game."""

    __tablename__ = "game_information"

    game_info_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=False)
    event_order = db.Column(db.Integer, nullable=False)
    game_description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)
    story_text = db.Column(db.Text, nullable=False)
    puzzle = db.Column(db.Text, nullable=False)
    puzzle_key = db.Column(db.Text, nullable=False)
    puzzle_hint = db.Column(db.Text, nullable=True)
    weather_condition = db.Column(db.String(64), nullable=True)

    #Define relationship to Games
    # game = db.relationship("Game",
    #                         backref=db.backref("games"))


#Functions to connect to database.

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///storytime'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    """Import app & connect to database as soon as file is run."""
    from server import app

    init_app()









