from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import line_app.settings as settings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)
migrate = Migrate(app, db)
