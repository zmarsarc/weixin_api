# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser
import requests
import json
import time


def singleton(cls):
    class wapped_class(cls):
        _instance = None
        
        def __new__(cls, *args, **kwargs):
            if wapped_class._instance is None:
                wapped_class._instance = super(wapped_class, cls).__new__(cls, *args, **kwargs)
            return wapped_class._instance

    return wapped_class


@singleton
class token(object):

    def __init__(self, config):
        self._config = config  # 保存获取 token 所需的配置信息，并且将 token 回写。

        self.__value = config.token
        self.update = config.update
        self.ttl = config.ttl

        if time.time() - self.update >= self.ttl:
            self.refresh()

    @property
    def value(self):
        if time.time() - self.update >= self.ttl:
            self.refresh()
        return self.__value

    def refresh(self):
        self.__value, self.ttl = self._get_token()
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
        self._config.token = self.__value
        self._config.ttl = self.ttl
        self._config.update = self.update
