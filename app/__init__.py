from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = "GHSDBVZTOTKAEFDCVBGHNJK"
app.static_folder = 'static'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

from app import views, models
