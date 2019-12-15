from json import dumps

from flask import Response


def json_response(data=None, code=200, msg=None, excluded_fields=()):
    # TODO: 加密
    if data is not None:
        if isinstance(data, list):
            resp = Response(dumps({'objects': data}),
                            status=code,
                            mimetype='application/json')
        else:
            resp = Response(dumps(data),
                            status=code,
                            mimetype='application/json')
    else:
        if msg:
            resp = Response(dumps({'errors': {}, 'msg': msg}),
                            status=code,
                            mimetype='application/json')
        else:
            resp = Response(dumps({}),
                            status=code,
                            mimetype='application/json')
    return resp
