"""Games"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, GameMaster, Player, Game, GameInfo, connect_to_db, db

import json

import os

import hashlib

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


@app.route('/process-registration', methods = ["POST"])
def register_process():
    """Find out whether user is in database or not and route accordingly."""

    fname = request.form.get("user_fname")
    lname = request.form.get("user_lname")
    username = request.form.get("username")
    email = request.form.get("user_email")
    password = request.form.get("user_password")
    security = request.form.get("security")
    sec_answer = request.form.get("security_answer")

    password = hashlib.sha256(password.encode("utf-8")).hexdigest()

    user_info = User.query.filter_by(email=email).all()

    all_games = db.session.query(Game).all()

    if user_info:
        flash("You've been here before - please log in to continue.")
        return render_template("login.html")
    else:
        new_user = User(fname=fname, lname=lname, username=username, email=email, password=password, security_question=security, security_answer=sec_answer)
        db.session.add(new_user)
        db.session.commit()

        session["active_session"] = new_user.user_id

        flash("Thank you for registering. Happy Gaming!")
        return render_template("mainpage.html",
                                username=username,
                                all_games=all_games)

@app.route('/login')
def login_page():
    """Take user to login page."""

    return render_template("login.html")


@app.route('/login-check', methods=["POST"])
def login_check():

    email = request.form.get("user_email")
    password = request.form.get("user_password")
    user_info = db.session.query(User.email, User.password, User.user_id).all()

    password = hashlib.sha256(password.encode("utf-8")).hexdigest()

    for user in user_info:
        if user[0] == email and user[1] == password:
            flash(u"Welcome Back!")
            flash("You're now logged in. Happy Gaming!")            
            session["active_session"] = user.user_id
            return redirect("/main-page")

    # If user credentials do not match database, we will flash a message and allow them to enter security question.
    flash(u"No account found for the entered email/password.")

    return render_template("login.html")


@app.route('/security-check')
def security_check():
    # Route that returns users security question and answer.

    email = request.args.get("email")
    results = db.session.query(User.security_question, User.security_answer).filter(User.email == email).all()

    return jsonify(results)

@app.route('/update-password', methods=["POST"])
def update_password():
    # Route that updates password inside database to new password from user.

    # Get user email and new password
    user_email = request.form.get("user_email")

    new_password = request.form.get("new_password")
    new_password = hashlib.sha256(new_password.encode("utf-8")).hexdigest()

    # Find user id in database using email as a filter
    user_info = User.query.filter_by(email=user_email).first()

    # Update password for the relevant user
    db.session.add(user_info)
    user_info.password = new_password
    db.session.commit()

    flash(u"Please log in with your newly updated password")

    return redirect("/login")

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
    # user_created_games = db.session.query(GameMaster.created_games).filter(GameMaster.user_id == session["active_session"]).all()

    # games_created = []

    # for game_id in all_games:
    #     game = db.session.query(Game).filter(Game.game_id == game_id)
    #     games_created.append(game.game_name)
    #     print(games_created)

    #This query pulls the current users' information.
    user_deets = db.session.query(User).filter(User.user_id == session["active_session"]).first()

    # This query pulls all the games players have played, along with their user_id (which we can use to pull user_id & usernames)
    # leaderboard_stats = db.session.query(Player.user_id, User.username, Player.games_played).join(User).all()

    # leaderboard_stats = db.session.query(Player.user_id, User.username, Player.games_played, Games.game_name).join(User).all()  


    # leaderboard_dict = {}

    # for user_id, username, games_played in leaderboard_stats:
    #     leaderboard_dict[(user_id, username)] = games_played

    # print(leaderboard_dict)
    # for user_id, username, games_played in leaderboard_stats:
    #     print(user_id)
    #     print(username)        
    #     print(games_played)
    #     print("\n\n")


    return render_template("mainpage.html",
                            all_games=all_games,
                            username = user_deets.username)
                            # user_games = user_created_games,
                            # leaderboard_stats=leaderboard_stats)

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

@app.route('/puzzle-key')
def get_game_puzzle_key():

    game_id = request.args.get('game_id')

    game_info = db.session.query(GameInfo.puzzle_key).filter(GameInfo.game_id == game_id).all()

    results = [ t[0] for t in game_info ]

    return jsonify(results)


@app.route('/record-game')
def record_game_completed():
    # Get game ID from game.html
    game_id = request.args.get('game_id')

    # Get user ID from session
    user_id = session['active_session']

    # Query to see if player and game are already in player database
    player_game_record = db.session.query(Player).filter(Player.user_id == user_id, Player.games_played == game_id).first()
    print(player_game_record)

    # If statement to add if record doesn't exist, flash message if already in database
    if player_game_record is None:
        alert_mssg = 'Congrats on solving this game!'

        record_game = Player(user_id=user_id, games_played=game_id)
        db.session.add(record_game)
        db.session.commit()
    else:
        alert_mssg = 'Congrats on solving this game again!'

    return jsonify(alert_mssg)

if __name__ == "__main__":
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app, db_uri='postgresql:///storytime')

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')    