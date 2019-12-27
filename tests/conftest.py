import json
from collections import namedtuple

import pendulum
import pytest

from app.extensions import pwdb
from app.poetry import models as poetry


class Client:
    METHODS = ["get", "post", "put", "delete"]

    def __init__(self, app):
        self.app = app
        self.client = app.test_client()
        self.set_user()

    def set_user(self, user_id=3):
        self.user_id = user_id
        self.user = namedtuple("User", ["id"])(self.user_id)
        payload = {
            "id": self.user.id,
            "username": "robot",
            "device": 0,
            "exp": str(pendulum.now().add(minutes=1)),
        }
        self.default_headers = {
            "content-type": "application/json",
            "x-user-payload": json.dumps(payload),
        }

    @staticmethod
    def handle_res(res, raw=False):
        if raw:
            return res

        if res.status_code not in (200, 400):
            return res.status_code, res.data

        return res.status_code, json.loads(res.data.decode() or "{}")

    def update_if_not_exist(self, custom_headers):
        headers = self.default_headers.copy()
        headers.update(custom_headers)
        return headers

    def get(self, url, raw=False, headers=None):
        if headers is None:
            headers = {}
        headers = self.update_if_not_exist(headers)
        return self.handle_res(self.client.get(url, headers=headers), raw)

    def post(self, url, data=None, raw=False, headers=None):
        if headers is None:
            headers = {}

        if data is None:
            data = {}

        headers = self.update_if_not_exist(headers)
        return self.handle_res(
            self.client.post(url, data=json.dumps(data), headers=headers), raw
        )

    def put(self, url, data=None, raw=False, headers=None):
        if headers is None:
            headers = {}

        if data is None:
            data = {}

        headers = self.update_if_not_exist(headers)
        return self.handle_res(
            self.client.put(url, data=json.dumps(data), headers=headers), raw
        )

    def delete(self, url, data=None, raw=False, headers=None):
        if headers is None:
            headers = {}

        if data is None:
            data = {}

        headers = self.update_if_not_exist(headers)
        return self.handle_res(
            self.client.delete(url, data=json.dumps(data), headers=headers), raw
        )


@pytest.fixture(scope="session")
def app():
    from app import app

    yield app


@pytest.fixture(scope="session")
def models():
    models = []
    for model in (poetry,):
        for i in model.__dict__.values():
            if isinstance(i, type) and issubclass(i,
                                                  pwdb.Model) and i is not pwdb.Model:
                models.append(i)

    yield models


@pytest.fixture(scope="session", autouse=True)
def db(models):
    with pwdb.database.atomic():
        pwdb.database.create_tables(models)

    yield

    with pwdb.database.atomic():
        pwdb.database.drop_tables(models)


@pytest.fixture(scope="function", autouse=True)
def data_cleaner(models):
    yield

    for model in models:
        model.delete().execute()


@pytest.fixture()
def client(app):
    obj = Client(app)

    yield obj
