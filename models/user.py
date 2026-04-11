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


def _get_user_columns(mysql):
    cur = mysql.connection.cursor()
    try:
        try:
            cur.execute("SHOW COLUMNS FROM users")
            rows = cur.fetchall()
            return [row[0] for row in rows]
        except Exception:
            cur.execute("PRAGMA table_info(users)")
            rows = cur.fetchall()
            return [row[1] for row in rows]
    finally:
        cur.close()


def get_user_by_email(mysql, email):
    columns = _get_user_columns(mysql)
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    record = dict(zip(columns, row))
    return {
        'id': record.get('id'),
        'name': record.get('name') or record.get('email', ''),
        'email': record.get('email'),
        'password_hash': record.get('password_hash') or record.get('password'),
        'role': record.get('role', 'admin'),
    }


def verify_password(stored_hash, password):
    if not stored_hash:
        return False

    if stored_hash.startswith(("pbkdf2:", "scrypt:")):
        return check_password_hash(stored_hash, password)

    return stored_hash == password
