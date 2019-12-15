from flask import Flask

from app.user.api import user


app = Flask(__name__)

app.register_blueprint(user, url_prefix="/user")
