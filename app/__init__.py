from flask import Flask, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config.update(dict(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'quickdashugahacks@gmail.com',
    MAIL_PASSWORD = 'inferno4lyfe',
    SECRET_KEY = 'any secret string'
	))
mail = Mail(app)


from app import routes, forms