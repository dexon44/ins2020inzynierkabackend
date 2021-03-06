import os

from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_admin import Admin

# Globally accessible libraries
db = SQLAlchemy()
ma = Marshmallow()
flask_adminer = Admin(name='adminekes')


def create_app():
    """Initalize the core application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Init Plugins
    db.init_app(app)
    flask_adminer.init_app(app)
    ma.init_app(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    from .models import User, UserSurvey, Book

    with app.app_context():
        # Import all blueprints
        from .user import user_routes
        from .book import book_routes
        from .survey import survey_routes
        from .flask_admin import flask_admin_routes

        # Register blueprints
        app.register_blueprint(user_routes.user_bp)
        app.register_blueprint(book_routes.book_bp)
        app.register_blueprint(survey_routes.survey_bp)
        app.register_blueprint(flask_admin_routes.flask_admin_bp)
        # db.drop_all()
        # db.create_all()

        # Create superuser
        # Create if statement for checking is superuser is already created
        if User.query.filter(User.superuser.is_(True)).first() is None:
            username = os.environ.get('superuser_nickname')
            email = os.environ.get('superuser_email')
            role = True
            superuser = True
            password_hash = generate_password_hash(os.environ.get('superuser_password'))
            superuser = User(username=username, email=email, role=role, superuser=superuser,
                             password_hash=password_hash)
            db.session.add(superuser)
            db.session.commit()

        return app
