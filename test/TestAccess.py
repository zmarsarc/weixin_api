# -*- coding: utf-8 -*-

import unittest
from multiprocessing import Process
from SampleServer import app
from api import Access
import time
import os
from api import Config


def start_server():
    # Process 需要一个 picklable 对象作为参数
    app.run(port=12345)


class TestAccess(unittest.TestCase):

    def setUp(self):
        self.server = Process(target=start_server)
        self.server.start()
        os.environ['WX_CONF_PATH'] = os.path.join(os.getcwd(), 'test\\Sample')
        self.config = Config.FileConfig('testserver.wxcfg')
        self.config.add('token', {'value': 'ACCESS_TOKEN_CACHE', 'ttl': '7200', 'update': str(int(time.time()))})
        self.config.add('appid', 'zmarsarc')
        self.config.add('secret', '123456')

    def test_get_token_cache(self):
        tk = Access.Token(self.config)
        self.assertEqual(self.config.get('token')['value'], tk.value)

    def test_get_token_new(self):
        token = self.config.get('token')
        token['update'] = 0
        self.config.set('token', token)
        tk = Access.Token(self.config)
        self.assertEqual('ACCESS_TOKEN', tk.value)

    def test_token_singleton(self):
        self.assertEqual(Access.Token(self.config), Access.Token(self.config))

    def tearDown(self):
        self.server.terminate()

if __name__ == '__main__':
    unittest.main()
