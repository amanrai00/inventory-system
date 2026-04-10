from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from MySQLdb import OperationalError
from models.user import get_user_by_email, verify_password
from functools import wraps

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        from flask import current_app
        mysql = current_app.extensions['mysql']

        try:
            user = get_user_by_email(mysql, email)
        except OperationalError:
            flash('Database connection failed. Check your MySQL settings in .env.', 'danger')
            return render_template('login.html'), 500

        if user and verify_password(user[3], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['user_role'] = user[4]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
