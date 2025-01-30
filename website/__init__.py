from flask import Flask, render_template
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '44'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # what this is doing is storing the DB_NAME database in the website folder 
    db.init_app(app) # what this is doing is taking database db, and telling it what app we are going to use

    from .views import views
    from .auth import auth

    return render_template('index.html')
