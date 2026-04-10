import sqlite3
from pathlib import Path


class SQLiteCursorWrapper:
    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, query, params=None):
        normalized_query = query.replace("%s", "?")
        if params is None:
            return self._cursor.execute(normalized_query)
        return self._cursor.execute(normalized_query, params)

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def close(self):
        self._cursor.close()


class SQLiteConnectionWrapper:
    def __init__(self, db_path: str):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(db_path, check_same_thread=False)
        self._connection.execute("PRAGMA foreign_keys = ON")

    def cursor(self):
        return SQLiteCursorWrapper(self._connection.cursor())

    def commit(self):
        self._connection.commit()

    def close(self):
        self._connection.close()


class SQLiteDBAdapter:
    def __init__(self, db_path: str):
        self.connection = SQLiteConnectionWrapper(db_path)
