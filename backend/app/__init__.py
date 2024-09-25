from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from celery import Celery
import redis


app = Flask(__name__, template_folder='template')

app.config['SECRET_KEY'] = 'THIS_IS_A_SECRET'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
celery.conf.update(app.config)

# celery.conf.update(
#     include=['app.name.tasks']
# )

db = SQLAlchemy(app)


CORS(app)

app.app_context().push()


from app.api import auth, post, follow, profile

from app.other import pdf


