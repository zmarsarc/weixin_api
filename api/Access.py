# -*- coding: utf-8 -*-
import requests
import json
import time
from .Utilties import Signleton
from .Logger import Logger
import os


class Token(object):

    __metaclass__ = Signleton

    def __init__(self, config):
        super(Token, self).__init__()

        self.logger = Logger.get_logger()
        self.config = config  # 保存获取 token 所需的配置信息，并且将 token 回写。
        with open(os.path.join(os.getcwd(), 'api\\data\\weixin.api')) as fp:
            self.api = json.load(fp)
            self.logger.info("module {0} read api file {1}".format(self.__class__, fp.name))
        self.token = self.config.get('token')
        self.__value = self.token['value']
        self.update = int(self.token['update'])
        self.ttl = int(self.token['ttl'])
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
        self.logger.info("refresh token, ttl {0}".format(self.ttl))
        self._set_config()

    def _get_token(self):
        params = {'grant_type': 'client_credential',
                  'appid': self.config.get('appid'),
                  'secret': self.config.get('secret')}
        response = requests.get(self.api["base"] + self.api['token']["api"], params=params)
        response = json.loads(response.content)
        return (response['access_token'], response['expires_in'])

    def _set_config(self):
        self.config.set('token', {"value": self.__value, "ttl": self.ttl, "update": self.update})
        self.logger.info("write token to config")
