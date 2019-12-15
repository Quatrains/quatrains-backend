
from flask.views import MethodView

from app.utils import json_response


class LoginView(MethodView):

    def get(self):
        return json_response({"res": "hello world"})
