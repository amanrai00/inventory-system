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
