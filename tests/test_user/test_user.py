

PREFIX = "/user"


def test_user_login(client):
    url = "{}/login".format(PREFIX)

    _, res = client.get(url)

    assert res["res"] == "hello world"
