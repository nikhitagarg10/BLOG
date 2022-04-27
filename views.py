from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if (request.method == "POST"):
        text = request.form.get("text")
        if not text:
            flash("Post cannnot be empty", category="error")
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created", category="successs")
            return redirect(url_for("views.home"))

    return render_template("create_post.html", user=current_user)

@views.route("/delete-post<id>")
@login_required
def delete_post(id):
    del_post = Post.query.filter_by(id=id).first()

    if not del_post:
        flash("Post does not exist", category="error")
    elif(current_user.id != del_post.author):
        flash("You do not have the permission to delete this post", category="error")
    else:
        db.session.delete(del_post)
        db.session.commit()
        flash("Post deleted", category="success")

    return redirect(url_for("views.home"))

@views.route("/profile/<username>")
@login_required
def posts(username):

    if (username == "self"):
        posts = current_user.posts
        posts = Post.query.filter_by(author=current_user.id).all()
        return render_template("profile.html", user=current_user, posts=posts, username=current_user.username)

    user = User.query.filter_by(username=username).first()

    if not user:
        flash("no user with that username exists", category="error")
        return redirect(url_for("views.home"))

    posts = user.posts
    return render_template("profile.html", user=current_user, posts=posts, username=username)

@views.route("/create-comment<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    text = request.form.get("text")

    if not text:
        flash("comment can not be empty", category="error")
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash("Post does not exist", category="error")

    return redirect(url_for("views.home")) 

@views.route("/delete-comment<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash("comment does not exist", category="error")
    elif(current_user.id != comment.author and current_user.id != comment.post.author):
        flash("you do not have the permission to delete the comment", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()
        flash("comment deleted successfully", category="success")
    
    return redirect(url_for("views.home")) 

@views.route("/like<post_id>", methods=["GET"])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id)
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        flash("post does not exist", category="error")
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return redirect(url_for("views.home"))

@views.route("/edit<post_id>", methods=["GET", "POST"])
@login_required
def edit(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if (request.method == "GET"):
        if not post:
            flash("This Post does not exists", category="error")
        elif (current_user.id != post.author):
            flash("you do not have the permission to edit this post", category="error")
        else:
            return render_template("edit_post.html", user=current_user, post=post)
    
    else:
        updated_post = request.form.get("text")

        if not updated_post:
            flash("A post can not be empty. PLease add some content", category="error")
        elif(updated_post == post):
            return redirect(url_for("views.home"))
        else:
            post.text = updated_post
            db.session.commit()
    return redirect(url_for("views.home"))