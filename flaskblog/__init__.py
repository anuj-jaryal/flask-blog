from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate



db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
toolbar = DebugToolbarExtension()
migrate = Migrate()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    from flaskblog.models import Tag

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    @app.context_processor
    def tags():
        return {tags:Tag.query.get()}

    return app;