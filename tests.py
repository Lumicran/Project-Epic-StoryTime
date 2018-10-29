import unittest
from server import app
from model import db, User, GameMaster, Player, Game, GameInfo, init_app, connect_to_db, test_data

################################################################################

# class StorytimeTestsDatabase(unittest.TestCase):
#     """Flask tests that use the database."""

#     def setUp(self):
#         """Setup before every test."""

#         self.client = app.test_client()
#         app.config['TESTING'] = True

#         # Connect to test database
#         connect_to_db(app, "postgresql:///testdb")

#         # Create tables and add sample data
#         db.create_all()
#         test_data()


#     def tearDown(self):
#         """Close out testing environment."""

#         db.session.close()
#         db.drop_all()
#         db.engine.dispose()

################################################################################

class Homepage(unittest.TestCase):
    """Tests for home page."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        test_data()


    def test_homepage(self):
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Register", result.data)


    def test_register(self):
        result = self.client.get("/register")
        self.assertIn(b"Registration Form", result.data)


    def test_login(self):
        result = self.client.get("/login")
        self.assertIn(b"Welcome Back!", result.data)
        self.assertNotIn(b"Register", result.data)


    def tearDown(self):
        """Close out testing environment."""

        db.session.close()
        db.drop_all()
        db.engine.dispose()    


################################################################################

class Registration(unittest.TestCase):
    """Tests for registration."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        test_data()


    def test_registered(self):
        result = self.client.post("/process-registration",
                                    data={"user_fname": "Ele",
                                    "user_lname": "Phant",
                                    "username": "elephant",
                                    "user_email": "elephant@gmail.com",
                                    "user_password": "elephant",
                                    "security": "pet",
                                    "security_answer": "Azula"},
                                    follow_redirects=True)

        result = self.client.get("/main-page")
  
        self.assertIn(b"Available Games", result.data)
        self.assertIn(b"elephant", result.data)

    def tearDown(self):
        """Close out testing environment."""

        db.session.close()
        db.drop_all()
        db.engine.dispose()    


################################################################################
class TestsLoggedIn(unittest.TestCase):
    """Tests on pages that require user log-in."""

    def setUp(self):
        """Setup, including starting user session."""
        self.client = app.test_client()
        app.config['TESTING'] = True   

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        test_data()     

        with self.client as c:
            with c.session_transaction() as session:
                session["active_session"] = 1


    def test_logged_in(self):
        result = self.client.post("/login",
                                    data={"email": "benneb",
                                    "password": "6700869c8ff7480e34a70a708b028700dbaa3a033b5652b903afe89f49a31456"},
                                    follow_redirects=True)
        result = self.client.get("/main-page")
        self.assertIn(b"Available Games", result.data)
        self.assertIn(b"benneb", result.data)

    def test_mainpage(self):
        """Tests for main page."""
        result = self.client.get("/main-page")
        self.assertIn(b"Games", result.data)


    def test_gamepage(self):
        result = self.client.get("/game-page?game_name=Cats%20Attack")
        self.assertIn(b"Game Page", result.data)


    def tearDown(self):
        """Close out testing environment."""

        db.session.close()
        db.drop_all()
        db.engine.dispose()    




if __name__ == "__main__":
    unittest.main()