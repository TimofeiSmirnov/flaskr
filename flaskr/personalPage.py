from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
pg = Blueprint('page', __name__)


@pg.route('/your-page')
def your_page():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    users_photo = db.execute(
        'SELECT p.user_id, photo, id'
        ' FROM users_photo p'
    ).fetchall()

    return render_template('page/yours.html', posts=posts, photo=users_photo)


def get_post_for_auto(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    return post


@pg.route('/<int:id>/person', methods=('GET', 'POST'))
@login_required
def person_page(id):
    post = get_post_for_auto(id)
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    if g.user is None:
        return render_template('page/person.html', posts=posts, per=None)
    elif g.user['id'] == post['author_id']:
        return render_template('page/yours.html', posts=posts)
    else:
        return render_template('page/person.html', posts=posts, per=post)


@pg.route('/photo', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        photo_for_user = request.form['photo']
        print(photo_for_user)
        error = None

        if not photo_for_user:
            error = 'The photo is not chosen.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO users_photo (photo, id)'
                ' VALUES (?, ?)',
                (photo_for_user, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

        return redirect(url_for('page/add_photo.html'))
    else:
        return render_template('page/add_photo.html')
