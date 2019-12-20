import json
import functools
from collections import namedtuple
import re

import jwt
import pendulum

from flask import Response, request, current_app


def json_response(data=None, code=200, msg=None, excluded_fields=()):
    # TODO: 加密
    if data is not None:
        if isinstance(data, list):
            resp = Response(json.dumps({'objects': data}),
                            status=code,
                            mimetype='application/json')
        else:
            resp = Response(json.dumps(data),
                            status=code,
                            mimetype='application/json')
    else:
        if msg:
            resp = Response(json.dumps({'errors': {}, 'msg': msg}),
                            status=code,
                            mimetype='application/json')
        else:
            resp = Response(json.dumps({}),
                            status=code,
                            mimetype='application/json')
    return resp


def permission_required(name="auth"):

    """
    :param name:  auth or admin
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = request.user
            if name not in ["auth", "admin"]:
                raise Exception("name {} is err".format(name))
            if name == "auth":
                if not user:
                    return json_response(code=401)
            if name == "admin":
                if not user or not user.is_staff:
                    return json_response(code=401, msg="has no permission")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def set_user_cookie(response):
    if getattr(request, "user", None) is None or response.status_code != 200:
        return response

    expire_seconds = current_app.config["JWT_EXPIRE_TIME"]
    expire_at = pendulum.now().add(seconds=expire_seconds)
    payload = {"id": request.user.id, "exp": expire_at, "device": ""}
    if hasattr(request.user, "username"):
        payload["username"] = request.user.username
    if hasattr(request.user, "is_staff"):
        payload["is_staff"] = request.user.is_staff

    auth_token = jwt.encode(payload, current_app.config["JWT_SECRET"])
    response.set_cookie(
        current_app.config["JWT_COOKIE_NAME"],
        auth_token,
        expires=expire_at,
        path=current_app.config["JWT_COOKIE_PATH"],
        domain=current_app.config["JWT_COOKIE_DOMAIN"],
        httponly=current_app.config["JWT_COOKIE_HTTPONLY"],
    )
    return response


def jwt_identify_parse():
    request.user = None

    try:
        payload = request.headers.get('x-user-payload')
        if payload:
            payload = json.loads(payload)

        else:
            cookie = request.headers.get("cookie")
            auth_token = re.findall("auth_token=(.*?);", str(cookie))[0]
            payload = jwt.decode(auth_token, current_app.config["JWT_SECRET"])

        request.user = namedtuple("User", payload.keys())(*payload.values())

    except Exception:
        return
