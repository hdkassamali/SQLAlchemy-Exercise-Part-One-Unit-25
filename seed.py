"""Seed file to make sample data for blogly db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# image_urls (so adding users doesn't look clunky)
lebron_image_url = "https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png"
jordan_image_url = "https://cdn.nba.com/manage/2021/08/michael-jordan-looks.jpg"
kobe_image_url = "https://cdn.nba.com/headshots/nba/latest/1040x760/977.png"

# Add users
lebron = User(first_name="Lebron", last_name="James", image_url=lebron_image_url)
jordan = User(first_name="Michael", last_name="Jordan", image_url=jordan_image_url)
kobe = User(first_name="Kobe", last_name="Bryant", image_url=kobe_image_url)

# Add new objects to session, so they'll persist
db.session.add_all([lebron, jordan, kobe])
# Commit--otherwise, this never gets saved!
db.session.commit()

# Add posts
lebron_post_1 = Post(title="2nd Best", content="He second to Mike.", user_id=1)
lebron_post_2 = Post(
    title="Leading Scorer", content="Most points of all time!", user_id=1
)
lebron_post_3 = Post(
    title="Part of Big Three",
    content="The leader of the Big 3 with Wade and Bosh.",
    user_id=1,
)
jordan_post_1 = Post(title="The GOAT", content="This man is the GOAT!", user_id=2)
jordan_post_2 = Post(title="6 Titles", content="He got 6, I repeat, 6!!", user_id=2)
kobe_post_1 = Post(title="Legend", content="Rip Kobe, miss you <3.", user_id=3)
kobe_post_2 = Post(title="Motivational", content="Love his speeches", user_id=3)

# Add new objects to session, so they'll persist
db.session.add_all(
    [
        lebron_post_1,
        lebron_post_2,
        lebron_post_3,
        jordan_post_1,
        jordan_post_2,
        kobe_post_1,
        kobe_post_2,
    ]
)
# Commit--otherwise, this never gets saved!
db.session.commit()
