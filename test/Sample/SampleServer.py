# -*- coding: utf-8 -*-

from flask import Flask, request, abort
import json

config = {
    'id': 'zmarsarc',
    'secret': '123456',
    'type': 'client_credential'
}

app = Flask('FakeServer')


@app.route('/cgi-bin/token')
def token():
    if request.method == 'GET' and is_params_valid(request.args):
        response = {
            'access_token': 'ACCESS_TOKEN',
            'expires_in': 7200
        }
        return json.JSONEncoder().encode(response)
    return abort(500)


def is_params_valid(params):
    try:
        return (params['grant_type'] == config['type'] and
                params['appid'] == config['id'] and
                params['secret'] == config['secret'])
    except KeyError:
        return False

app.run(port=12345)
