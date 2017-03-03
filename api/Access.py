# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser
import requests
import json
import time


class token(object):

    def __init__(self, config):
        self._config = config  # 保存获取 token 所需的配置信息，并且将 token 回写。

        self.value = config.token
        self.update = config.update
        self.ttl = config.ttl

        if int(time.time()) - self.update >= self.ttl:
            self.refresh()

    def refresh(self):
        self.value, self.ttl = self._get_token()
        self.update = int(time.time())
        self._set_config()

    def _get_token(self):
        params = {'grant_type': 'client_credential',
                  'appid': self._config.id,
                  'secret': self._config.secret}
        response = requests.get(self._config.api, params=params)
        response = json.loads(response.content)
        return (response['access_token'], response['expires_in'])

    def _set_config(self):
       pass
