from .jwt import *  # noqa
from .peewee import *  # noqa

APP_SECRET = ""
APP_ID = ""

SWAGGER_DOCS_PATH = "docs"
SWAGGER = {
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}


TZ = "Asia/Shanghai"
