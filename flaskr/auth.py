from flask import Blueprint, render_template, request, flash, url_for, redirect, session
from werkzeug.security import generate_password_hash
from flaskr.db import get_db

blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@blueprint.route('signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']    
        password = request.form['password']
        db = get_db()
        error = None
        if not username:
            error = 'Username is required'
        elif not password:
            erorr = 'Password is required'
        if error is None:
            try: 
                db.execute(
                    "INSERT INTO user (username, password) (?, ?)",
                    (username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f'{username} is already taken'
            else: 
                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/signup.html')

@blueprint.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute("SELECT * FROM users WHERE username = ?", username).fetchone()
        correct_password = check_password_hash(user['password'], password)

        if user is None or not correct_password: 
            error = 'Invalid username or password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')
