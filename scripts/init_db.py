import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config
from database.client import SQLiteDBAdapter

if Config.DB_BACKEND == "mysql":
    import MySQLdb


def split_sql_statements(sql_text: str) -> list[str]:
    statements = []
    current = []

    for line in sql_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            continue
        current.append(line)
        if stripped.endswith(";"):
            statements.append("\n".join(current).strip().rstrip(";"))
            current = []

    if current:
        statements.append("\n".join(current).strip().rstrip(";"))

    return statements


def ensure_prediction_columns(cursor, db_backend: str) -> None:
    if db_backend == "mysql":
        cursor.execute("SHOW TABLES LIKE 'predictions'")
        if not cursor.fetchone():
            return

        cursor.execute("SHOW COLUMNS FROM predictions")
        existing_columns = {row[0] for row in cursor.fetchall()}
        if "reason_en" not in existing_columns:
            cursor.execute("ALTER TABLE predictions ADD COLUMN reason_en TEXT NULL")
        if "reason_ja" not in existing_columns:
            cursor.execute("ALTER TABLE predictions ADD COLUMN reason_ja TEXT NULL")
        return

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='predictions'"
    )
    if not cursor.fetchone():
        return

    cursor.execute("PRAGMA table_info(predictions)")
    existing_columns = {row[1] for row in cursor.fetchall()}
    if "reason_en" not in existing_columns:
        cursor.execute("ALTER TABLE predictions ADD COLUMN reason_en TEXT")
    if "reason_ja" not in existing_columns:
        cursor.execute("ALTER TABLE predictions ADD COLUMN reason_ja TEXT")


def main() -> None:
    load_dotenv()

    if Config.DB_BACKEND == "mysql":
        connection = MySQLdb.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            passwd=Config.MYSQL_PASSWORD,
            charset="utf8mb4",
        )
        schema_path = PROJECT_ROOT / "database" / "schema.sql"
    else:
        connection = SQLiteDBAdapter(Config.SQLITE_PATH).connection
        schema_path = PROJECT_ROOT / "database" / "schema_sqlite.sql"

    schema_sql = schema_path.read_text(encoding="utf-8")

    cursor = connection.cursor()
    if Config.DB_BACKEND == "mysql":
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.MYSQL_DB}`")
        connection.select_db(Config.MYSQL_DB)

    for statement in split_sql_statements(schema_sql):
        cursor.execute(statement)

    ensure_prediction_columns(cursor, Config.DB_BACKEND)

    connection.commit()
    cursor.close()
    connection.close()

    if Config.DB_BACKEND == "mysql":
        print(f"MySQL database '{Config.MYSQL_DB}' is ready.")
    else:
        print(f"SQLite database is ready at '{Config.SQLITE_PATH}'.")
    print("Default admin email: admin@company.com")
    print("Default admin password: admin123")


if __name__ == "__main__":
    main()
