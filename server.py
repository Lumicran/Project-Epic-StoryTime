"""Games"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, GameMaster, Player, Game, GameInfo, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

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

        return render_template("mainpage.html")


@app.route('/login')
def login_page():
    """Take user to login page."""

    return render_template("login.html")


@app.route('/login-check')
def login_check():

    email = request.args.get("user_email")
    password = request.args.get("user_password")
    user_info = db.session.query(User.email, User.password, User.user_id).all()

    for user in user_info:
        if user[0] == email and user[1] == password:
            flash(u"Welcome Back!")
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

    flash("You're now logged in. Happy Gaming!")

    return render_template("mainpage.html")

@app.route('/create-game')
def create_game_page():
    """Page shown where GM's can create a game."""

    return render_template("game_creation.html")

@app.route('/game-shell', methods=["POST"])
def game_shell_creation():
    """This gets the puzzle/game details from game_creation.html)"""

    game_title = request.form.get("game_title")
    game_info = db.session.query(Game.game_id, Game.game_name).all()

    for game in game_info:
        if game_title == game[1]:
            flash(u"This game already exists. Please create a new game.")
            return redirect("/create-game")
        else:
            #Adding game to Games table in storytime DB.
            new_game = Game(game_name=game_title)
            db.session.add(new_game)
            db.session.commit()

    return render_template("game_details.html")


@app.route('/game-details', methods=["POST"])
def get_game_details():
    """Route to record game details for an event."""

    game_description = request.form.get("game_description")
    event_order = request.form.get("event_order")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    story_text = request.form.get("story_text")
    puzzle = request.form.get("puzzle")    
    puzzle_key = request.form.get("puzzle_key")
    puzzle_hint = request.form.get("puzzle_hint")
    weather_condition = request.form.get("weather_condition")

    #Query to get game ID for particular game ||||| BUILD!!!!
    game_id = db.session.query(Game.game_id).all()

    #Adding event to Game Information table.
    game_item = GameInfo(game_id=game_id, event_order=event_order, game_description=game_description, latitude=latitude,
                    longitude=longitude, story_text=story_text, puzzle=puzzle, puzzle_key=puzzle_key,
                    puzzle_hint=puzzle_hint, weather_condition=weather_condition)
    db.session.add(game_item)
    db.session.commit()

    return render_template("game_details.html") 



if __name__ == "__main__":
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')    