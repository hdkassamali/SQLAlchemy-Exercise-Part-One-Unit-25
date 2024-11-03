"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Default_pfp.svg/1024px-Default_pfp.svg.png"

# When working in ipython, running seed file, or when using unittest framework use this connect_db function otherwise use the one below:
# def connect_db(app):
#     db.app = app
#     db.init_app(app)


def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()


class User(db.Model):
    """Site Users."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(25), nullable=False)

    last_name = db.Column(db.String(25), nullable=False)

    image_url = db.Column(db.String(255), nullable=False, default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}. id: {self.id} >"


class Post(db.Model):
    """Blog Posts."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.String(10000), nullable=False)

    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", backref="posts")

    def __repr__(self):
        return f"<Post_info -> id: {self.id}, title: {self.title}, user_id: {self.user_id} >"
