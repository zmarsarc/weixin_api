# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser
import requests
import json
import time


class token(object):

    def __init__(self):
        self.value = None
        self.update = None
        self.ttl = None

        self._config = self._get_config()  # 保存获取 token 所需的配置信息，并且将 token 回写。

    def refresh(self):
        self.value, self.ttl = self._get_token()
        self.update = int(time.time())
        self._set_config()

    def _get_token(self):
        params = {'grant_type': 'client_credential',
                  'appid': self._config.appid,
                  'secret': self._config.secret}
        response = requests.get(self._config.token_api, params=params)
        response = json.loads(response.content)
        return (response['access_token'], response['expires_in'])

    def _get_config(self):
        configer = ConfigParser()
        configer.read('config.cfg')
        ret = object()
        ret.token_api = 'https://api.weixin.qq.com/cgi-bin/token'
        ret.appid = configer.get('App_info', 'id')
        ret.secret = configer.get('App_info', 'secret')
        return ret

    def _set_config(self):
        raise NotImplemented('Access.token._set_config not implemented')
