from flask import Blueprint

from app.recommend.api import views as v


recommend = Blueprint("recommend", __name__)

recommend.add_url_rule(
    "daily_poetry", view_func=v.DailyPoetryView.as_view("daily_poetry"),
    methods=["GET"]
)
