"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "blogproject12345"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

# When working in ipython, running seed file, or when using unittest framework run the line below:
# app.app_context().push()

connect_db(app)


@app.route("/")
def root():
    """Homepage redirects to list of users."""

    return redirect("/users")


# USERS ROUTES
@app.route("/users")
def homepage():
    """Show a page with info on all users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/users/new")
def new_user_form():
    """Show a form to create a new user"""

    return render_template("new_user_form.html")


@app.route("/users/new", methods=["POST"])
def add_new_user():
    """Handle form submission for creating a new user"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"] or None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def user_details(user_id):
    """Show a page with info on a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)


@app.route("/users/<int:user_id>/edit")
def user_edit_page(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template("user_edit_page.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_details(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)

    # Delete all posts and their associations by querying and deleting each post.
    for post in user.posts:
        PostTag.query.filter_by(post_id=post.id).delete()
        Post.query.filter_by(id=post.id).delete()

    db.session.delete(user)

    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def show_post_form(user_id):
    """Show the form for a user to create a post."""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("post_form.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_new_post(user_id):
    """Add the user's post to their page."""

    title = request.form["title"]
    content = request.form["content"]
    selected_tags = request.form.getlist("tags")

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    for tag_id in selected_tags:
        post_tag = PostTag(post_id=new_post.id, tag_id=tag_id)
        db.session.add(post_tag)

    db.session.commit()

    return redirect(f"/users/{user_id}")


# POSTS ROUTES
@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show post details for a specific post"""

    post = Post.query.get_or_404(post_id)

    return render_template("post_details.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Show form to edit a post."""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template("edit_post_form.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Handle the editing of a post."""

    post = Post.query.get_or_404(post_id)

    # update the title and content
    post.title = request.form["title"]
    post.content = request.form["content"]
    selected_tags = request.form.getlist("tags")

    db.session.add(post)
    db.session.commit()

    # Get current tag IDs associated with the post
    current_tag_ids = [tag.id for tag in post.tags]

    # convert selected Tag Ids to integers.
    selected_tag_ids = [int(tag_id) for tag_id in selected_tags]

    # Add new tags that aren't already in post.tags
    for tag_id in selected_tag_ids:
        if tag_id not in current_tag_ids:
            post_tag = PostTag(post_id=post_id, tag_id=tag_id)
            db.session.add(post_tag)

    # remove tags that are no longer selected
    for tag_id in current_tag_ids:
        if tag_id not in selected_tag_ids:
            PostTag.query.filter_by(post_id=post_id, tag_id=tag_id).delete()

    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete a post"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user.id

    # Remove association from PostTag table
    PostTag.query.filter_by(post_id=post_id).delete()

    # Delete Post
    db.session.delete(post)

    db.session.commit()

    return redirect(f"/users/{user_id}")


# TAGS ROUTES
@app.route("/tags")
def list_tags():
    """List all Tags."""

    tags = Tag.query.all()
    return render_template("list_tags.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    """Show details about a tag."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_details.html", tag=tag)


@app.route("/tags/new")
def add_tag_form():
    """Show form to add a new tag"""

    return render_template("add_tag.html")


@app.route("/tags/new", methods=["POST"])
def add_new_tag():

    new_tag = Tag(name=request.form["name"])

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    """Show form to edit a tag."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Process edit tag form."""

    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form["name"]

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag."""

    PostTag.query.filter_by(tag_id=tag_id).delete()

    Tag.query.filter_by(id=tag_id).delete()

    db.session.commit()

    return redirect("/tags")
