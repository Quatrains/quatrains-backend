

PREFIX = "/user"


def test_user_login(client):
    url = f"{PREFIX}/login"

    _, res = client.get(url)

    assert res["res"] == "hello world"
