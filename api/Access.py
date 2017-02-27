# -*- coding: utf-8 -*-


class token(object):

    def __init__(self):
        self.value = None
        self.update = None
        self.ttl = None

        self._config = None  # 保存获取 token 所需的配置信息，并且将 token 回写。

    def refresh(self):
        pass

    def _get_token(self):
        pass

    def _get_config(self):
        pass
