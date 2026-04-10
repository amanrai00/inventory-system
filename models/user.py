from werkzeug.security import generate_password_hash, check_password_hash


def create_user(mysql, name, email, password, role='employee'):
    cur = mysql.connection.cursor()
    password_hash = generate_password_hash(password)
    cur.execute(
        "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
        (name, email, password_hash, role)
    )
    mysql.connection.commit()
    cur.close()


def get_user_by_email(mysql, email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    return user


def verify_password(stored_hash, password):
    return check_password_hash(stored_hash, password)
