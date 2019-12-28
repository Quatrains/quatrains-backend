
from app.poetry import models as m


def test_user_login(client, mocker, app):
    mk_oauth_get_access_token = mocker.patch("app.poetry.models.wechatmp_oauth.get_access_token")
    mk_oauth_get_access_token.return_value = {
        "session_key": "",
        "openid": "1234"
    }

    url = "user/login"

    payload = {
        "code": "1234"
    }

    # register if not exist
    code, _ = client.post(url, data=payload)

    assert code == 200
    mk_oauth_get_access_token.assert_called_with(app.config["APP_ID"],
                                                 app.config["APP_SECRET"],
                                                 payload["code"])
    wechat_user = m.WechatUser.get(open_id="1234")
    assert wechat_user
    user = m.User.get(id=wechat_user.user_id)
    assert user

    # login again
    code, _ = client.post(url, data=payload)

    assert code == 200
    assert m.WechatUser.select().where(m.WechatUser.open_id == "1234").count() == 1
    assert m.User.select().count() == 1


def test_get_profile(client, user):
    url = "user/profile"

    _, res = client.get(url)

    assert "have_interests" in res
    assert "join_days" in res


def test_list_user_favorites(client, poetry, user_favorite):
    url = "/user/favorite?page=1&ipp=10"

    _, res = client.get(url)

    assert res["total"] == 1
    assert res["objects"][0]["id"] == poetry.id


def test_add_user_favorite(client, poetry):
    url = "/user/favorite"
    payload = {
        "poetry_id": poetry.id
    }

    code, res = client.post(url, payload)

    assert code == 200
    assert m.UserFavorite.select().where(
        m.UserFavorite.user_id == client.user_id,
        m.UserFavorite.poetry_id == poetry.id
    ).exists() is True


def test_list_interests(client, interest):
    url = "/interests"

    _, res = client.get(url)

    assert res["objects"][0]["text"] == interest.text


def test_add_interests(client, interest):
    url = "/user/interests"
    payload = {
        "interest_ids": [interest.id]
    }

    code, res = client.post(url, payload)

    assert code == 200
    assert m.UserInterest.select().where(
        m.UserInterest.user_id == client.user_id
    ).exists() is True


def test_get_daily_poetry(client, poetry):
    url = "/daily_poetry"

    _, res = client.get(url)

    assert "week" in res
    assert "today_date" in res
    assert res["poetry"]["id"] == poetry.id
