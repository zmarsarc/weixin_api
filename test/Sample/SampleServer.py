# -*- coding: utf-8 -*-

from flask import Flask, request
import json


app = Flask('FakeServer')


@app.route('/cgi-bin/token')
def token():
    if request.method == 'GET':
        response = {
            'access_token': 'ACCESS_TOKEN',
            'expires_in': 7200
        }
        return json.JSONEncoder().encode(response)

app.run(port=12345)
