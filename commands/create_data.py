import json

from app.poetry.models import *


def import_poetry(filename):
    with open(filename, "r", encoding="utf8") as f:
        poems = json.load(f)

    cnt = 0
    for poem in poems:
        try:
            Poetry.create(
                idx=poem["idx"],
                title=poem["title"],
                title_tr=poem["titleTr"],
                author=poem["author"],
                author_tr=poem["authorTr"],
                content=poem["content"],
                content_tr=poem["contentTr"],
                background=poem["background"] or "",
                analysis=poem["analysis"] or ""
            )
        except Exception as err:
            print(err)
        cnt += 1

        if cnt % 100 == 0:
            print("process: {}".format(cnt))

    print("done...")


def import_interest(filename):
    with open(filename, "r", encoding="utf8") as f:
        interests = json.load(f)

    cnt = 0
    for inte in interests:
        Interest.create(
            text=inte
        )
        cnt += 1

        if cnt % 100 == 0:
            print("process: {}".format(cnt))

    print("done...")
