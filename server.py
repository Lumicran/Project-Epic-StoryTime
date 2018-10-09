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

@app.route('/main-page')
def main_page():
    """Main page shown once a user logs in."""

    return render_template("mainpage.html")





if __name__ == "__main__":
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')    