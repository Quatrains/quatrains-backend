import os

from flask import Flask
from werkzeug.utils import import_string

from app.user.api import user
from app.recommend.api import recommend
from app.utils import jwt_identify_parse, set_user_cookie


app = Flask(__name__)

env = os.environ.get('FLASK_ENV', 'development')
config = import_string('configs.{}'.format(env))
app.config.from_object(config)

app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(recommend, url_prefix="/recommend")

app.before_request(jwt_identify_parse)
app.after_request(set_user_cookie)
