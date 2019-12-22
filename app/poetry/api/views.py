from collections import namedtuple

from flask.views import MethodView
from flask import request

from app.utils import json_response, swag_from_yml_file, permission_required


class LoginView(MethodView):

    @swag_from_yml_file("login_post.yml")
    def post(self):
        data = request.json

        code = data["code"]

        request.user = namedtuple("User", ["id", "is_staff", "username"])(
            1, 1, "robot12"
        )

        return json_response()


class ProfileView(MethodView):

    @swag_from_yml_file("profile_get.yml")
    @permission_required()
    def get(self):
        pass


class FavoriteView(MethodView):

    @swag_from_yml_file("favorite_list.yml")
    @permission_required()
    def get(self):
        pass

    @swag_from_yml_file("favorite_post.yml")
    @permission_required()
    def post(self):
        pass


class InterestsView(MethodView):

    @swag_from_yml_file("interests_list.yml")
    @permission_required()
    def get(self):
        pass


class UserInterestsView(MethodView):

    @swag_from_yml_file("user_interests_post.yml")
    @permission_required()
    def post(self):
        pass


class DailyPoetryView(MethodView):

    @swag_from_yml_file("daily_poetry_get.yml")
    @permission_required()
    def get(self):
        pass
