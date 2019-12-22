import os
import inspect

from flask import Flask
from werkzeug.utils import import_string

from app.utils import jwt_identify_parse, set_user_cookie

root_path = os.getcwd()
app = Flask(__name__, root_path=root_path)
env = os.environ.get('FLASK_ENV', 'development')
config = import_string('configs.{}'.format(env))
app.config.from_object(config)

# load extensions
exts_module = import_string("app.extensions")
for n, ext in inspect.getmembers(
        exts_module,
        lambda ins: not inspect.isclass(ins) and hasattr(ins, 'init_app')):
    ext.init_app(app)
    app.extensions[n] = exts_module

from app.poetry.api import bp  # noqa

app.register_blueprint(bp, url_prefix="/")

app.before_request(jwt_identify_parse)
app.after_request(set_user_cookie)
