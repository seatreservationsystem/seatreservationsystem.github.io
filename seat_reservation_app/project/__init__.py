# init.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

from .seatMakerEdited import seatMakerEdited
from .seat import seat
import os
import mysql.connector



# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # So images aren't cached
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

        # Should match roomMaps directory in seatMakerEdited.py
    mDIR = "static/roomMaps/"

    # Create .csv and .svg directories
    seatMakerEdited.makeCSVDIR()
    seatMakerEdited.makeMAPDIR()

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
