"""Seed file to make sample data for blogly db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# image_urls (so adding users doesn't look clunky)
lebron_image_url = "https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png"
jordan_image_url = "https://cdn.nba.com/manage/2021/08/michael-jordan-looks.jpg"
kobe_image_url = "https://cdn.nba.com/headshots/nba/latest/1040x760/977.png"

# Add users
lebron = User(first_name="Lebron", last_name="James", image_url=lebron_image_url)
jordan = User(first_name="Michael", last_name="Jordan", image_url=jordan_image_url)
kobe = User(first_name="Kobe", last_name="Bryant", image_url=kobe_image_url)

# Add new objects to session, so they'll persist
db.session.add(lebron)
db.session.add(jordan)
db.session.add(kobe)

# Commit--otherwise, this never gets saved!
db.session.commit()
