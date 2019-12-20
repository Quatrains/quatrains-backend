

PREFIX = "/user"


def test_user_login(client):
    url = "{}/login".format(PREFIX)

    payload = {
        "code": "1234"
    }

    code, _ = client.post(url, data=payload)

    assert code == 200


