from collections import namedtuple

from flask.views import MethodView
from flask import request

from app.utils import json_response


class LoginView(MethodView):

    def post(self):
        data = request.json

        code = data["code"]

        request.user = namedtuple("User", ["id", "is_staff", "username"])(
            1, 1, "robot12"
        )

        return json_response()
