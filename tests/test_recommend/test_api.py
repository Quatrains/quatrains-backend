

PREFIX = "/recommend"


def test_get_daily_poetry(client):
    url = "{}/daily_poetry".format(PREFIX)

    _, res = client.get(url)

    assert res["poetry"]
