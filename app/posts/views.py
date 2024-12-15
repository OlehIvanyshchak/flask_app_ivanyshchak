from flask import render_template, abort, flash, redirect, url_for, session
from . import post_bp
from .forms import PostForm
import os
import json

JSON_DB = "app/posts/posts.json"


def load_posts():
    if os.path.exists(JSON_DB):
        with open(JSON_DB, "r") as f:
            return json.load(f)
    return []


def save_posts(posts):
    with open(JSON_DB, "w") as f:
        json.dump(posts, f, indent=4, default=str)


@post_bp.route("/")
def get_posts():
    posts = load_posts()
    return render_template("posts.html", posts=posts)


@post_bp.route("/<int:id>")
def get_post(id):
    posts = load_posts()
    post = next((post for post in posts if post["id"] == id), None)
    if post is None:
        abort(404)
    return render_template("detail-post.html", post=post)


@post_bp.route("/add_post", methods=["GET", "POST"])
def add_post():
    if "username" not in session:
        flash("Please login to add a post", "danger")
        return redirect(url_for("users.login"))

    form = PostForm()
    if form.validate_on_submit():
        posts = load_posts()

        new_post = {
            "id": len(posts) + 1,
            "title": form.title.data,
            "content": form.content.data,
            "is_active": form.is_active.data,
            "publish_date": form.publish_date.data,
            "category": form.category.data,
            "author": session["username"],
        }
        posts.append(new_post)
        save_posts(posts)

        flash("Post added successfully", "success")
        return redirect(url_for("posts.get_posts"))
    return render_template("add_post.html", form=form)
