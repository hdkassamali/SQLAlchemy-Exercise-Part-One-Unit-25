from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_ECHO"] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add a sample user."""

        User.query.delete()

        user = User(
            first_name="Michael",
            last_name="Jordan",
            image_url="https://cdn.nba.com/manage/2021/08/michael-jordan-looks.jpg",
        )

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_users_list(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Michael Jordan", html)

    def test_add_new_user(self):
        with app.test_client() as client:
            data = {
                "first_name": "Lebron",
                "last_name": "James",
                "image_url": "https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png",
            }

            resp = client.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Lebron James", html)

    def test_edit_user_data(self):
        with app.test_client() as client:
            self.user.first_name = "Kobe"
            self.user.last_name = "Bryant"
            self.user.image_url = (
                "https://cdn.nba.com/headshots/nba/latest/1040x760/977.png"
            )

            data = {
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "image_url": self.user.image_url,
            }

            resp = client.post(
                f"/users/{self.user_id}/edit", data=data, follow_redirects=True
            )

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Kobe Bryant", html)
            self.assertNotIn("Michael Jordan", html)

    def test_delete_user(self):
        with app.test_client() as client:
            data = {
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "image_url": self.user.image_url,
            }

            resp = client.post(
                f"users/{self.user_id}/delete", data=data, follow_redirects=True
            )

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Michael Jordan", html)
