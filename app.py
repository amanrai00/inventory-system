from flask import Flask, redirect, url_for
from flask_mysqldb import MySQL
from config import Config
from database.client import SQLiteDBAdapter

mysql = MySQL()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    if Config.DB_BACKEND == 'mysql':
        app.config['MYSQL_HOST'] = Config.MYSQL_HOST
        app.config['MYSQL_PORT'] = Config.MYSQL_PORT
        app.config['MYSQL_USER'] = Config.MYSQL_USER
        app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
        app.config['MYSQL_DB'] = Config.MYSQL_DB

        mysql.init_app(app)
        app.extensions['mysql'] = mysql
    else:
        app.extensions['mysql'] = SQLiteDBAdapter(Config.SQLITE_PATH)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.products import products_bp
    from routes.sales import sales_bp
    from routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(dashboard_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
