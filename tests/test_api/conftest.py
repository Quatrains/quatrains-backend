
import pytest

from app.poetry import models as m


@pytest.fixture()
def user(client):
    obj = m.User.create(
        id=client.user_id,
        username="poetry"
    )

    yield obj

    obj.delete_instance()


@pytest.fixture()
def poetry():
    obj = m.Poetry.create(
        idx=1,
        title="静夜思",
        author="李白",
        content=[
            "床前明月光，",
            "疑是地上霜。",
            "举头望明月，",
            "低头思故乡。"
        ]
    )

    yield obj


@pytest.fixture()
def user_favorite(client, poetry):
    obj = m.UserFavorite.create(
        user_id=client.user_id,
        poetry_id=poetry.id
    )

    yield obj

    obj.delete_instance()


@pytest.fixture()
def interest():
    obj = m.Interest.create(
        text="送别"
    )

    yield obj

    obj.delete_instance()
