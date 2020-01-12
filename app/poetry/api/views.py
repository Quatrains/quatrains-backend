from flask.views import MethodView
from flask import request

from app.utils import json_response, swag_from_yml_file, permission_required
from app.poetry import models as m


class LoginView(MethodView):

    @swag_from_yml_file("login_post.yml")
    def post(self):
        data = request.json
        code = data["code"]

        wechat_user = m.WechatUser.get_or_create_by_mp_code(code)

        request.user = wechat_user.user

        return json_response()


class ProfileView(MethodView):

    @swag_from_yml_file("profile_get.yml")
    @permission_required()
    def get(self):
        user_id = request.user.id

        profile = m.UserProfile.get_profile(user_id)

        return json_response(profile)


class FavoriteView(MethodView):

    @swag_from_yml_file("favorite_list.yml")
    @permission_required()
    def get(self):
        user_id = request.user.id
        data = request.args
        page = int(data.get("page", 1))
        ipp = int(data.get("ipp", 10))

        total = m.UserFavorite.select().where(m.UserFavorite.user_id == user_id).count()
        favorites = m.UserFavorite.list_favorites(user_id, page, ipp)

        data = {
            "total": total,
            "page": page,
            "ipp": ipp,
            "objects": favorites
        }

        return json_response(data)

    @swag_from_yml_file("favorite_post.yml")
    @permission_required()
    def post(self):
        user_id = request.user.id
        data = request.json
        poetry_id = data["poetry_id"]

        m.UserFavorite.add_favorite(user_id, poetry_id)

        return json_response()


class InterestsView(MethodView):

    @swag_from_yml_file("interests_list.yml")
    @permission_required()
    def get(self):
        data = request.args
        page = int(data.get("page", 1))
        ipp = int(data.get("ipp", 10))

        total = m.Interest.select().count()
        interests = m.Interest.list_interests(page, ipp)

        data = {
            "total": total,
            "page": page,
            "ipp": ipp,
            "objects": interests
        }

        return json_response(data)


class UserInterestsView(MethodView):

    @swag_from_yml_file("user_interests_post.yml")
    @permission_required()
    def post(self):
        user_id = request.user.id
        data = request.json
        interest_ids = data["interest_ids"]

        m.UserInterest.add_interests(user_id, interest_ids)

        return json_response()


class DailyPoetryView(MethodView):

    @swag_from_yml_file("daily_poetry_get.yml")
    @permission_required()
    def get(self):
        user_id = request.user.id

        poetry = m.Poetry.get_daily_poetry(user_id)

        return json_response(poetry)


class LoginFreeView(MethodView):

    def post(self):
        user = m.User.get(username="robot1")
        request.user = user

        return json_response()

    def get(self):
        user = m.User.get(username="robot1")
        request.user = user

        return json_response()
