"""Games"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, GameMaster, Player, Game, GameInfo, connect_to_db, db

import json

import os

app = Flask(__name__)

app.secret_key = os.environ["SECRET_KEY"]

# If an undefined variable is used in Jinja2, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register')
def route_to_form():
    """Take user to registration page"""

    return render_template("registration.html")


@app.route('/process-registration', methods =["POST"])
def register_process():
    """Find out whether user is in database or not and route accordingly."""

    fname = request.form.get("user_fname")
    lname = request.form.get("user_lname")
    username = request.form.get("username")
    email = request.form.get("user_email")
    password = request.form.get("user_password")

    user_info = User.query.filter_by(email=email).all()

    if user_info:
        flash("You've been here before - please log in to continue.")
        return render_template("login.html")
    else:
        new_user = User(fname=fname, lname=lname, username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        session["active_session"] = new_user.user_id

        flash("Thank you for registering. Happy Gaming!")
        return render_template("mainpage.html")


@app.route('/login')
def login_page():
    """Take user to login page."""

    return render_template("login.html")


@app.route('/login-check', methods=["POST"])
def login_check():

    email = request.form.get("user_email")
    password = request.form.get("user_password")
    user_info = db.session.query(User.email, User.password, User.user_id).all()

    for user in user_info:
        if user[0] == email and user[1] == password:
            flash(u"Welcome Back!")
            flash("You're now logged in. Happy Gaming!")            
            session["active_session"] = user.user_id
            return redirect("/main-page")
        else:
            continue

    flash(u"No account found for the entered email/password.")
    return render_template("login.html")


@app.route('/logout')
def logout_page():
    """Take user to login page."""

    session.pop('active_session')
    flash("You are now logged out.")

    return redirect("/")


@app.route('/main-page')
def main_page():
    """Main page shown once a user logs in."""

    all_games = db.session.query(Game).all()

    #This query receives a list of game id's that a user has created.
    #user_created_games = db.session.query(GameMaster.created_games).filter(GameMaster.user_id == session["active_session"]).all()

    # games_created = []

    # for game_id in user_created_games:
    #     game = db.session.query(Game).filter(Game.game_id == game_id)
    #     games_created.append(game.game_name)
    #     print(games_created)

    #This query pulls the current users' information.
    user_deets = db.session.query(User).filter(User.user_id == session["active_session"]).first()

    return render_template("mainpage.html",
                            all_games=all_games,
                            username = user_deets.username)
                            # user_games = user_created_games)

# @app.route('/create-game')
# def create_game_page():
#     """Page shown where GM's can create a game."""

#     user_id = session['active_session']

#     return render_template("game_creation.html")

# @app.route('/game-shell', methods=["POST"])
# def game_shell_creation():
#     """This gets the puzzle/game details from game_creation.html)"""

#     game_title = request.form.get("game_title")
#     game_description = request.form.get("game_description")

#     game_info = db.session.query(Game.game_id, Game.game_name).all()

#     # for game in game_info:
#     #     if game_title == game[1]:
#     #         flash(u"This game already exists. Please create a new game.")
#     #         return redirect("/create-game")

    
#     #Adding game to Games table in storytime DB.
#     new_game = Game(game_name=game_title, game_description=game_description)
#     db.session.add(new_game)
#     db.session.commit()

#     user_id = session["active_session"]
#     created_game = new_game.game_id

#     gm_record = GameMaster(user_id=user_id, created_games=created_game)
#     db.session.add(gm_record)
#     db.session.commit()

#     session['current_game'] = created_game

#     return render_template("game_details.html",
#                             game_id=created_game,
#                             game_name=new_game.game_name)


# @app.route('/game-details', methods=["POST"])
# def get_game_details():
#     """Route to record game details for an event."""

#     game_id = session['current_game']

#     game_name = db.session.query(Game.game_name).filter(Game.game_id == game_id).first()
#     game_name = game_name[0]

#     event_order = request.form.get("event_order")
#     latitude = request.form.get("latitude")
#     longitude = request.form.get("longitude")
#     story_text = request.form.get("story_text")
#     puzzle = request.form.get("puzzle")    
#     puzzle_key = request.form.get("puzzle_key")
#     puzzle_hint = request.form.get("puzzle_hint")
#     weather_condition = request.form.get("weather_condition")

#     #Adding event to Game Information table.
#     game_item = GameInfo(game_id=game_id, event_order=event_order, latitude=latitude,
#                     longitude=longitude, story_text=story_text, puzzle=puzzle, puzzle_key=puzzle_key,
#                     puzzle_hint=puzzle_hint, weather_condition=weather_condition)
#     db.session.add(game_item)
#     db.session.commit()

#     #Pulling game details
#     game_details = db.session.query(GameInfo).filter(GameInfo.game_id == game_id).all()

#     return render_template("game.html",
#                             game_id=game_id,
#                             game_name=game_name,
#                             game_details=game_details) 

@app.route('/game-page')
def show_game():
    """Route to game page."""

    game_name = request.args.get('game_name')

    game = db.session.query(Game).filter(Game.game_name == game_name).one()

    game_id = game.game_id
    game_description = game.game_description

    game_info = db.session.query(GameInfo).filter(GameInfo.game_id == game_id).all()

    # Code to pass in puzzle key as json so we can use it in JavaScript
    puzzle_key = []
    hints = []
    location_hint = []
    coordinates = []

    for game in game_info:
        puzzle_key.append(game.puzzle_key)
        hints.append(game.puzzle_hint)
        location_hint.append(game.location_hint)

        latitude = float(game.latitude)
        longitude = float(game.longitude)
        coordinates.append([latitude, longitude])

    gkey = os.environ['GKEY']

    print("\n\n\n\n\n\n")
    print(coordinates)
    print("\n\n\n\n\n\n")

    return render_template("game.html",
                            game_id=game_id,
                            game_name=game_name,
                            game_description=game_description,
                            game_info=game_info,
                            puzzle_key=puzzle_key,
                            hints=hints,
                            location_hint=location_hint,
                            gkey=gkey,
                            coordinates=coordinates)




if __name__ == "__main__":
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')    