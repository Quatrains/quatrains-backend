import os

from flask import Flask
from werkzeug.utils import import_string

from app.user.api import user


app = Flask(__name__)

env = os.environ.get('FLASK_ENV', 'development')
config = import_string('configs.{}'.format(env))
app.config.from_object(config)

app.register_blueprint(user, url_prefix="/user")
