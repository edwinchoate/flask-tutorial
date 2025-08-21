import functools
from flask import g, Blueprint, render_template, request, flash, url_for, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.db import get_db
from sqlite3 import IntegrityError

blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']    
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        db = get_db()
        error = None
        if not username:
            error = 'Username is required'
        elif not password or not confirm_password:
            error = 'Password is required'
        elif password != confirm_password:
            error = 'Passwords do not match'
        if error is None:
            try: 
                db.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                db.commit()
            except IntegrityError:
                error = f'{username} is already taken'
            else: 
                return redirect(url_for('auth.login'))
        flash(error)
        return render_template('auth/signup.html', username=username)
    return render_template('auth/signup.html')

@blueprint.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user is None or not check_password_hash(user['password'], password): 
            error = 'Invalid username or password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
        return render_template('auth/login.html', username=username)
    return render_template('auth/login.html')


@blueprint.route('/logout')
def logout(): 
    session.clear()
    return redirect(url_for('auth.login'))


@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is not None:
        user = get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        g.user = user
    else:
        g.user = None


# This creates a decorator that you can use to require login for a given view function
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        else: 
            return view(**kwargs)
    return wrapped_view
