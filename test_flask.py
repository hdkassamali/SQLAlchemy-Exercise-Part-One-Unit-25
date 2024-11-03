from unittest import TestCase

from app import app
from models import db, User, Post

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

        Post.query.delete()
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

            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Michael Jordan", html)


class PostViewsTestCase(TestCase):
    """Test for views for posts."""

    def setUp(self):
        """Add a sample user. And two sample posts"""

        Post.query.delete()
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

        post_1 = Post(
            title="The Goat", content="He's the greatest.", user_id=self.user_id
        )
        post_2 = Post(
            title="Scoring Titles",
            content="He has 10 scoring titles",
            user_id=self.user_id,
        )

        db.session.add_all([post_1, post_2])
        db.session.commit()

        self.post_1 = post_1
        self.post_1_id = post_1.id

        self.post_2 = post_2
        self.post_2_id = post_2.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_user_posts(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Michael Jordan", html)
            self.assertIn("The Goat", html)
            self.assertIn("Scoring Titles", html)

    def test_add_post(self):
        with app.test_client() as client:
            data = {
                "title": "6 Rings",
                "content": "2 back2back2backs.",
                "user_id": self.user_id,
            }

            resp = client.post(
                f"/users/{self.user_id}/posts/new", data=data, follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("6 Rings", html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_2_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Scoring Titles", html)
            self.assertIn("He has 10 scoring titles", html)

    def test_edit_post(self):
        with app.test_client() as client:
            self.post_1.title = "Scottie Pippen"
            self.post_1.content = "He was his fave teammate."

            data = {
                "title": self.post_1.title,
                "content": self.post_1.content,
                "user_id": self.user_id,
            }

            resp = client.post(
                f"/posts/{self.post_1_id}/edit", data=data, follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Scottie Pippen", html)
            self.assertNotIn("greatest", html)
            self.assertNotIn("Goat", html)

    def test_delete_post(self):
        with app.test_client() as client:

            resp = client.post(f"/posts/{self.post_2_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Scoring Titles", html)
            self.assertIn("The Goat", html)
