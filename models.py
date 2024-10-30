"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# When working in ipython or when using unittest framework use this connect_db function otherwise use the one below:
# def connect_db(app):
#     db.app = app
#     db.init_app(app)


def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)

    first_name = db.Column(db.String(25), nullable=False)

    last_name = db.Column(db.String(25), nullable=False)

    image_url = db.Column(db.String(255), nullable=True)
