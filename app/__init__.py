import os

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

# Gblobally accessible libraries
db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    """Initalize the core application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Init Plugins
    db.init_app(app)
    ma.init_app(app)

    from .models import User, UserSurvey

    with app.app_context():
        # Import all blueprints
        # from .admin import admin_routes
        # from .rest_jwt import jwt_rest_routes
        # from .user import user_routes
        # from .services import services_routes

        # Register blueprints
        # app.register_blueprint(admin_routes.admin_bp)
        # app.register_blueprint(jwt_rest_routes.jwt_rest_bp)
        # app.register_blueprint(user_routes.user_bp)
        # app.register_blueprint(services_routes.services_bp)
        db.drop_all()
        db.create_all()

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

