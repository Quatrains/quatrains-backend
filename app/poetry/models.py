from enum import unique, IntEnum
import uuid
import random

import peewee as pw
from peeweext.fields import JSONCharField
from flask import current_app
import pendulum

from app.extensions import pwdb, predict
from app.oauth import wechatmp_oauth


@unique
class ThirdParty(IntEnum):
    WECHAT_MP = 0


class WechatUser(pwdb.Model):
    user_id = pw.BigIntegerField()
    open_id = pw.CharField(max_length=128, unique=True)
    app_id = pw.CharField(max_length=128, index=True)
    union_id = pw.CharField(max_length=128, null=True, index=True)

    class Meta:
        table_name = "wechat_user"

    @property
    def user(self):
        return User[self.user_id]

    @classmethod
    def get_by_app_id_open_id(cls, app_id, open_id):
        return cls.get(cls.app_id == app_id,
                       cls.open_id == open_id)

    @classmethod
    def _create_by_app_id_open_id(cls, app_id, open_id, third_party):
        with pwdb.database.atomic():
            user = User.create_user_by_third_party(third_party)

            wechat_user = cls.create(
                user_id=user.id,
                open_id=open_id,
                app_id=app_id
            )

        return wechat_user

    @classmethod
    def get_or_create_by_mp_code(cls, code):
        app_id = current_app.config["APP_ID"]
        app_secret = current_app.config["APP_SECRET"]

        open_id = wechatmp_oauth.get_access_token(app_id, app_secret, code)["openid"]

        try:
            wechat_user = cls.get_by_app_id_open_id(app_id, open_id)

        except pw.DoesNotExist:

            wechat_user = cls._create_by_app_id_open_id(app_id, open_id, ThirdParty.WECHAT_MP)

        return wechat_user


class User(pwdb.Model):
    avatar_url = pw.CharField(max_length=256, default="")
    username = pw.CharField(max_length=32, unique=True)
    nickname = pw.CharField(max_length=32, default="")
    status = pw.SmallIntegerField(default=0)
    password_hash = pw.CharField(max_length=128, default="")

    class Meta:
        table_name = "user"

    @property
    def join_days(self):
        today = pendulum.today(tz=current_app.config["TZ"])
        return (today - self.created_at).days

    @classmethod
    def create_user_by_third_party(cls, third_party):

        user = None
        for _ in range(3):
            username = cls.gen_username(third_party)
            try:
                user = cls.create(
                    username=username
                )
                break

            except pw.IntegrityError:
                continue

        if user is None:
            raise Exception("注册失败，请重试")

        return user

    @classmethod
    def gen_username(cls, third_party):
        prefix = ThirdParty(third_party).name.capitalize()
        random_str = uuid.uuid4().hex[16:]
        return "{}_{}".format(prefix, random_str)


class Interest(pwdb.Model):
    text = pw.CharField(max_length=32, unique=True)

    class Meta:
        table_name = "interest"

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text
        }

    @classmethod
    def list_interests(cls, page, ipp):
        interests = cls.select().paginate(page, ipp)
        return [i.to_dict() for i in interests]


class Poetry(pwdb.Model):
    # 推荐系统产出的诗歌id为idx
    idx = pw.IntegerField(unique=True)
    title = pw.CharField(max_length=32)
    title_tr = pw.CharField(max_length=32, default="")
    author = pw.CharField(max_length=32)
    author_tr = pw.CharField(max_length=32, default="")
    content = JSONCharField(max_length=4096, default=list)
    content_tr = JSONCharField(max_length=4096, default=list)
    background = pw.CharField(max_length=2048, default="")
    analysis = pw.TextField(default="")

    class Meta:
        table_name = "poetry"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "content": self.content
        }

    @classmethod
    def get_daily_poetry(cls, user_id):
        today_date = pendulum.today(tz=current_app.config["TZ"]).date()
        poetry = cls.recommend_a_poetry(user_id)

        return {
            "today_date": str(today_date),
            "week": today_date.day_of_week,
            "poetry": poetry.to_dict()
        }

    @classmethod
    def _random_fetch_a_poetry(cls, user_id):
        total = Poetry.select().count()

        pidx = random.randint(0, total-1)
        poetry = Poetry.select().paginate(pidx, 1).first()

        return poetry

    @classmethod
    def recommend_a_poetry(cls, user_id):
        user_interest = UserInterest.get_user_interest(user_id)
        interests = [
            i.text for i in Interest.select().where(Interest.id.in_(user_interest.interest_ids))
        ]

        user_favorites = UserFavorite.select().where(UserFavorite.user_id == user_id).limit(30)
        poetries = Poetry.select().where(
            Poetry.id.in_([i.poetry_id for i in user_favorites])
        )
        favorite_poetry_idx = [i.idx for i in poetries]

        idx = predict.predict(interests, favorite_poetry_idx, [])
        return Poetry.get(idx=idx)


class UserFavorite(pwdb.Model):
    @unique
    class Type(IntEnum):
        POETRY = 0

    user_id = pw.BigIntegerField(index=True)
    poetry_id = pw.IntegerField()
    type = pw.SmallIntegerField(default=Type.POETRY)

    class Meta:
        table_name = "user_favorite"
        indexes = ((("user_id", "poetry_id"), True),)

    @classmethod
    def list_favorites(cls, user_id, page=1, ipp=10):
        favs = cls.select().where(
            cls.user_id == user_id
        ).paginate(page, ipp)

        poetries = Poetry.select().where(
            Poetry.id.in_([i.poetry_id for i in favs])
        )

        return [i.to_dict() for i in poetries]

    @classmethod
    def add_favorite(cls, user_id, poetry_id):
        cls.create(
            user_id=user_id,
            poetry_id=poetry_id
        )


class UserInterest(pwdb.Model):
    user_id = pw.BigIntegerField(unique=True)
    interest_ids = JSONCharField(max_length=512, default=list)

    class Meta:
        table_name = "user_interest"

    @classmethod
    def check_have_interests(cls, user_id):
        ui = cls.select().where(cls.user_id == user_id).first()

        if ui and ui.interest_ids != []:
            return True

        return False

    @classmethod
    def add_interests(cls, user_id, interest_ids):
        cls.create(
            user_id=user_id,
            interest_ids=interest_ids
        )

    @classmethod
    def get_user_interest(cls, user_id):
        ui, _ = cls.get_or_create(user_id=user_id)

        return ui


class UserProfile:

    @classmethod
    def get_profile(cls, user_id):
        user = User[user_id]

        have_interests = UserInterest.check_have_interests(user_id)

        return {
            "have_interests": have_interests,
            "join_days": user.join_days
        }
