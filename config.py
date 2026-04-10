import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'
    DB_BACKEND = os.getenv('DB_BACKEND', 'sqlite').lower()
    MYSQL_HOST = os.getenv('DB_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('DB_PORT', 3306))
    MYSQL_USER = os.getenv('DB_USER', 'root')
    MYSQL_PASSWORD = os.getenv('DB_PASSWORD', '')
    MYSQL_DB = os.getenv('DB_NAME', 'inventory_db')
    SQLITE_PATH = os.getenv('SQLITE_PATH', os.path.join(BASE_DIR, 'instance', 'inventory.db'))
