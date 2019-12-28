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
        interests = m.Interest.list_interests()

        data = {
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


class AutoCreateDataView(MethodView):

    def get(self):
        from app.extensions import pwdb
        pwdb.database.create_tables([
            m.WechatUser, m.User,
            m.Interest, m.Poetry,
            m.UserInterest, m.UserFavorite
        ])

        m.WechatUser.delete().execute()
        m.User.delete().execute()
        m.Interest.delete().execute()
        m.Poetry.delete().execute()
        m.UserInterest.delete().execute()
        m.UserFavorite.delete().execute()

        m.User.create(
            username="robot1"
        )

        for text in ["爱", "禅", "诗", "酒", "战争", "离别", "悼亡", "思乡"]:
            m.Interest.create(text=text)

        m.Poetry.create(
            idx=1,
            title="春望",
            author="杜甫",
            content=[
                "国破山河在，",
                "城春草木深。",
                "感时花溅泪，",
                "恨别鸟惊心。",
                "烽火连三月，",
                "家书抵万金。",
                "白头搔更短，",
                "浑欲不胜簪。"
            ]
        )

        m.Poetry.create(
            idx=2,
            title="别董大（其一）",
            author="高适",
            content=[
                "千里黄云白日曛，",
                "北风吹雁雪纷纷。",
                "莫愁前路无知己，",
                "天下谁人不识君。"
            ]
        )

        m.Poetry.create(
            idx=3,
            title="赠范晔",
            author="陆凯",
            content=[
                "折花逢驿使，",
                "寄与陇头人。",
                "江南无所有，",
                "聊赠一枝春。"
            ]
        )

        m.Poetry.create(
            idx=4,
            title="小重山",
            author="岳飞",
            content=[
                "昨夜寒蛩不住鸣。",
                "惊回千里梦，",
                "已三更。",
                "起来独自绕阶行。",
                "人悄悄，",
                "帘外月胧明。",
                "白首为功名。",
                "旧山松竹老，",
                "阻归程。",
                "欲将心事付瑶琴，",
                "知音少，",
                "弦断有谁听？"
            ]
        )

        m.Poetry.create(
            idx=5,
            title="浣溪沙",
            author="纳兰性德",
            content=[
                "谁念西风独自凉，",
                "萧萧黄叶闭疏窗，",
                "沉思往事立残阳。",
                "被酒莫惊春睡重，",
                "赌书消得泼茶香，",
                "当时只道是寻常。"
            ]
        )

        return json_response({"res": "创建成功"})


class LoginFreeView(MethodView):

    def post(self):
        user = m.User.get(username="robot1")
        request.user = user

        return json_response()

    def get(self):
        user = m.User.get(username="robot1")
        request.user = user

        return json_response()
