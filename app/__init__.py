from flask import Flask, make_response
from flask_login import LoginManager

from app.extensions import db

from app import secret

from app.main.models import User


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SECRET_KEY'] = secret.SECRET_KEY
    app.secret_key = secret.SECRET_KEY

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'main.konkurs_talantov_login'
    login_manager.init_app(app)

    @app.errorhandler(404)
    def err_404(e):
        return make_response('<h1>404</h1><br/><p>Не найдено.</p>', 404)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

