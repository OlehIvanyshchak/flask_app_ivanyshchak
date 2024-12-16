from flask import render_template, abort, flash, redirect, url_for, session
from . import post_bp
from .forms import PostForm
from app.posts.models import Post, Tag
from app import db
from app.users.models import User


@post_bp.route("/")
def get_posts():
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template("posts.html", posts=posts)


@post_bp.route("/<int:id>")
def get_post(id):
    post = Post.query.get(id)
    if post is None:
        abort(404)
    return render_template("detail-post.html", post=post)


@post_bp.route("/add_post", methods=["GET", "POST"])
def add_post():
    form = PostForm()
    authors = User.query.all()
    tags = Tag.query.all()
    form.author_id.choices = [(author.id, author.username) for author in authors]
    form.tags.choices = [(tag.id, tag.name) for tag in tags]
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.publish_date.data,
            is_active=form.is_active.data,
            category=form.category.data,
            user_id=form.author_id.data,
        )
        tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        new_post.tags.extend(tags)
        db.session.add(new_post)
        db.session.commit()

        flash("Post added successfully", "success")
        return redirect(url_for("posts.get_posts"))
    return render_template("add_post.html", form=form)


@post_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    form.publish_date.data = post.posted
    authors = User.query.all()
    tags = Tag.query.all()
    form.author_id.choices = [(author.id, author.username) for author in authors]
    form.tags.choices = [(tag.id, tag.name) for tag in tags]

    if not form.is_submitted():
        form.tags.data = [tag.id for tag in post.tags]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.posted = form.publish_date.data
        post.is_active = form.is_active.data
        post.category = form.category.data
        post.user_id = form.author_id.data
        tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        post.tags = tags
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for(".get_posts"))
    return render_template("edit-post.html", form=form, post=post)


@post_bp.route("/delete/<int:id>", methods=["POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully", "success")
    return redirect(url_for(".get_posts"))
