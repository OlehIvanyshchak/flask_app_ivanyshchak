from flask import render_template, abort
from . import post_bp

posts = [
    {
        "id": 1,
        "title": "My First Post",
        "content": "This is the content of my first post.",
        "author": "John Doe",
    },
    {
        "id": 2,
        "title": "Another Day",
        "content": "Today I learned about Flask macros.",
        "author": "Jane Smith",
    },
    {
        "id": 3,
        "title": "Flask and Jinja2",
        "content": "Jinja2 is powerful for templating.",
        "author": "Mike Lee",
    },
]


@post_bp.route("/")
def get_posts():
    return render_template("posts/posts.html", posts=posts)


@post_bp.route("/<int:id>")
def get_post(id):
    if id > len(posts):
        abort(404)
    post = posts[id - 1]
    return render_template("posts/detail-post.html", post=post)
