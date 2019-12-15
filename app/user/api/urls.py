from flask import Blueprint

from app.user.api import views as v

user = Blueprint("user", __name__)

user.add_url_rule(
    "login", view_func=v.LoginView.as_view("login"),
    methods=["GET"]
)
