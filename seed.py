"""Seed file to make sample data for blogly db."""

from models import User, Post, PostTag, Tag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

# image_urls (so adding users doesn't look clunky)
lebron_image_url = "https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png"
jordan_image_url = "https://cdn.nba.com/manage/2021/08/michael-jordan-looks.jpg"
kobe_image_url = "https://cdn.nba.com/headshots/nba/latest/1040x760/977.png"
ant_image_url = "https://cdn.nba.com/headshots/nba/latest/1040x760/1630162.png"
jokic_image_url = "https://cdn.nba.com/headshots/nba/latest/1040x760/203999.png"
steph_image_url = "https://cdn.nba.com/headshots/nba/latest/1040x760/201939.png"

# Add users
users = [
    User(first_name="Lebron", last_name="James", image_url=lebron_image_url),
    User(first_name="Michael", last_name="Jordan", image_url=jordan_image_url),
    User(first_name="Kobe", last_name="Bryant", image_url=kobe_image_url),
    User(first_name="Anthony", last_name="Edwards", image_url=ant_image_url),
    User(first_name="Nikola", last_name="Jokic", image_url=jokic_image_url),
    User(first_name="Stephen", last_name="Curry", image_url=steph_image_url),
]

# Add new objects to session, so they'll persist
db.session.add_all(users)
# Commit--otherwise, this never gets saved!
db.session.commit()

# Add posts
posts = [
    Post(title="2nd Best", content="He second to Mike.", user_id=1),
    Post(title="Leading Scorer", content="Most points of all time!", user_id=1),
    Post(
        title="Part of Big Three",
        content="The leader of the Big 3 with Wade and Bosh.",
        user_id=1,
    ),
    Post(title="The GOAT", content="This man is the GOAT!", user_id=2),
    Post(title="6 Titles", content="He got 6, I repeat, 6!!", user_id=2),
    Post(
        title="10 Scoring Titles",
        content="No one else has more than 4 I believe.",
        user_id=2,
    ),
    Post(title="Legend", content="Rip Kobe, miss you <3.", user_id=3),
    Post(title="Motivational", content="Love his speeches", user_id=3),
    Post(
        title="Same Beast?",
        content="Are you a different animal and the same beast?",
        user_id=3,
    ),
    Post(title="Athlete", content="The man always posterizes Yuta Watanabe", user_id=4),
    Post(title="Funny Guy", content="Told Jettas he can tackle King Henry", user_id=4),
    Post(title="Big Pony", content="I Joker ride big big horsey.", user_id=5),
    Post(
        title="Sure, Basketball",
        content="I guess I'll play your silly american game.",
        user_id=5,
    ),
    Post(title="Splash", content="Best shooter the Earth has ever seen", user_id=6),
    Post(title="Misses Klay", content="Broken up from your boy :(", user_id=6),
]
# Add new objects to session, so they'll persist
db.session.add_all(posts)
# Commit--otherwise, this never gets saved!
db.session.commit()

# Add Tags
tags = [
    Tag(name="Funny"),
    Tag(name="Informative"),
    Tag(name="Crazy"),
    Tag(name="Cool"),
    Tag(name="Random"),
]


# Add new objects to session, so they'll persist
db.session.add_all(tags)
# Commit--otherwise, this never gets saved!
db.session.commit()

# add relationships
# Define post-tag pairs as tuples
post_tag_pairs = [
    (1, 1),
    (1, 3),
    (2, 4),
    (3, 2),
    (5, 1),
    (5, 3),
    (6, 3),
    (7, 3),
    (9, 1),
    (9, 5),
    (10, 5),
    (10, 1),
    (11, 1),
    (12, 1),
    (12, 5),
    (13, 5),
    (13, 3),
    (14, 2),
    (15, 5),
]

post_tags = [
    PostTag(post_id=post_id, tag_id=tag_id) for post_id, tag_id in post_tag_pairs
]
# Add new objects to session, so they'll persist
db.session.add_all(post_tags)
# Commit--otherwise, this never gets saved!
db.session.commit()
