"""Utility file to seed storytime database from data in seed file."""

from sqlalchemy import func
from model import User, GameMaster, Player, Game, GameInfo
from model import init_app, connect_to_db, db
from server import app
import hashlib


def load_users():
    """Load users from u.user into database."""

    print("Users")

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, fname, lname, username, email, password, security_question, security_answer = row.split("|")
        
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        user = User(user_id=user_id,
                    fname=fname,
                    lname=lname,
                    username=username,
                    email=email,
                    password=password,
                    security_question=security_question,
                    security_answer=security_answer)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_gms():
    """Load gms from u.gm into database."""

    print("Game Masters")

    # Delete all rows in table to streamline second upload.
    # GameMaster.query.delete()

    # Read u.gm file and parse information.

    for row in open("seed_data/u.gm"):
        row = row.rstrip()
        gm_id, user_id, created_games = row.split("|")

        gm = GameMaster(gm_id=gm_id, user_id=user_id, created_games=created_games)

        db.session.add(gm)

    db.session.commit()


def load_players():
    """Load players from u.player into database."""

    print("Players")

    # Player.query.delete()

    for row in open("seed_data/u.player"):
        row = row.rstrip()
        player_id, user_id, games_played, games_not_played = row.split("|")

        player = Player(player_id=player_id,
                        user_id=user_id,
                        games_played=games_played,
                        games_not_played=games_not_played)

        db.session.add(player)

    db.session.commit()

def load_games():
    """Load games from u.game into database."""

    print("Games")

    # Game.query.delete()

    for row in open("seed_data/u.game"):
        row = row.rstrip()
        game_id, game_name, game_description = row.split("|")

        game = Game(game_id=game_id,
                    game_name=game_name,
                    game_description=game_description)

        db.session.add(game)
        
    db.session.commit()

def load_game_details():
    """Load game details from u.gameinfo into database."""

    print("Game Info")

    # GameInfo.query.delete()

    for row in open("seed_data/u.gameinfo"):
        row = row.rstrip()
        game_info_id, game_id, event_order, latitude, longitude, location_hint, story_text, puzzle, puzzle_key, puzzle_hint, weather_condition = row.split("|")

        gameinfo = GameInfo(game_info_id=game_info_id,
                            game_id=game_id,
                            event_order=event_order,
                            latitude=latitude,
                            longitude=longitude,
                            location_hint=location_hint,
                            story_text=story_text,
                            puzzle=puzzle,
                            puzzle_key=puzzle_key,
                            puzzle_hint=puzzle_hint,
                            weather_condition=weather_condition)

        db.session.add(gameinfo)
        
    db.session.commit()



def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_gm_id():
    """Set value for the next gm_id after seeding database"""

    # Get the Max gm_id in the database
    result = db.session.query(func.max(GameMaster.gm_id)).one()
    max_id = int(result[0])

    # Set the value for the next gm_id to be max_id + 1
    query = "SELECT setval('game_masters_gm_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_player_id():
    """Set value for the next player_id after seeding database"""

    # Get the Max player_id in the database
    result = db.session.query(func.max(Player.player_id)).one()
    max_id = int(result[0])

    # Set the value for the next gm_id to be max_id + 1
    query = "SELECT setval('players_player_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_game_id():
    """Set value for the next game_id after seeding database"""

    # Get the Max game_id in the database
    result = db.session.query(func.max(Game.game_id)).one()
    max_id = int(result[0])

    # Set the value for the next gm_id to be max_id + 1
    query = "SELECT setval('games_game_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()    

def set_val_gameinfo_id():
    """Set value for the next game_info_id after seeding database"""

    # Get the Max game_info_id in the database
    result = db.session.query(func.max(GameInfo.game_info_id)).one()
    max_id = int(result[0])

    # Set the value for the next gm_id to be max_id + 1
    query = "SELECT setval('game_information_game_info_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()    


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    GameMaster.query.delete()
    Player.query.delete()
    User.query.delete()
    GameInfo.query.delete()
    Game.query.delete()
    load_users()
    load_games()
    load_gms()
    load_players()
    load_game_details()
    set_val_user_id()
    set_val_gm_id()
    set_val_player_id()
    set_val_game_id()
    set_val_gameinfo_id()
