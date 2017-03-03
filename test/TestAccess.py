# -*- coding: utf-8 -*-

import unittest
from multiprocessing import Process
from SampleServer import app
from api import Access
import time


def start_server():
    # Process 需要一个 picklable 对象作为参数
    app.run(port=12345)


class TestAccess(unittest.TestCase):

    class config:
        api = 'http://127.0.0.1:12345/cgi-bin/token'
        token = 'ACCESS_TOKEN_CACHE'
        ttl = 7200
        update = int(time.time())
        id = 'zmarsarc'
        secret = '123456'

    def setUp(self):
        self.server = Process(target=start_server)
        self.server.start()

    def test_get_token_cache(self):
        tk = Access.token(self.config)
        self.assertEqual(self.config.token, tk.value)

    def test_get_token_new(self):
        config = self.config()
        config.update = 0
        tk = Access.token(config)
        self.assertEqual('ACCESS_TOKEN', tk.value)

    def test_token_auto_update(self):
        config = self.config()
        config.ttl = 1
        tk = Access.token(config)
        self.assertEqual('ACCESS_TOKEN_CACHE', tk.value)
        time.sleep(1)
        self.assertEqual('ACCESS_TOKEN', tk.value)

    def tearDown(self):
        self.server.terminate()

if __name__ == '__main__':
    unittest.main()
