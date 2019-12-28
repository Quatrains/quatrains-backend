from flask import Blueprint

from app.poetry.api import views as v

bp = Blueprint("api", __name__)

bp.add_url_rule(
    "user/login", view_func=v.LoginView.as_view("login"),
    methods=["POST"]
)

bp.add_url_rule(
    "user/profile", view_func=v.ProfileView.as_view("profile"),
    methods=["GET"]
)

bp.add_url_rule(
    "user/favorite", view_func=v.FavoriteView.as_view("favorite"),
    methods=["GET", "POST"]
)

bp.add_url_rule(
    "user/interests", view_func=v.UserInterestsView.as_view("user_interests"),
    methods=["POST"]
)

bp.add_url_rule(
    "interests", view_func=v.InterestsView.as_view("interests"),
    methods=["GET"]
)


bp.add_url_rule(
    "daily_poetry", view_func=v.DailyPoetryView.as_view("daily_poetry"),
    methods=["GET"]
)


# temp, delete when production
bp.add_url_rule(
    "auto_create_data", view_func=v.AutoCreateDataView.as_view("auto_create_data"),
    methods=["GET"]
)

bp.add_url_rule(
    "user/login_free", view_func=v.LoginFreeView.as_view("login_free"),
    methods=["POST", "GET"]
)