from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from MySQLdb import OperationalError
from models.user import get_user_by_email, verify_password
from functools import wraps
from config import Config

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
    form_data = {'email': ''}
    field_errors = {}
    general_error = None

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        form_data['email'] = email

        if not email:
            field_errors['email'] = 'Email is required.'

        if not password:
            field_errors['password'] = 'Password is required.'

        if field_errors:
            return render_template(
                'login.html',
                field_errors=field_errors,
                form_data=form_data,
                general_error=general_error
            ), 400

        from flask import current_app
        mysql = current_app.extensions['mysql']

        try:
            user = get_user_by_email(mysql, email)
        except OperationalError:
            if Config.AUTH_UI_PREVIEW:
                general_error = 'Invalid email or password.'
                return render_template(
                    'login.html',
                    field_errors=field_errors,
                    form_data=form_data,
                    general_error=general_error
                )
            flash('Database connection failed. Check your MySQL settings in .env.', 'danger')
            return render_template('login.html'), 500

        if user and verify_password(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.dashboard'))
        else:
            general_error = 'Invalid email or password.'

    return render_template(
        'login.html',
        field_errors=field_errors,
        form_data=form_data,
        general_error=general_error
    )


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
