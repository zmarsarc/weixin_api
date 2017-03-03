# -*- coding: utf-8 -*-

import unittest
from multiprocessing import Process
from SampleServer import app


def start_server():
    # Process 需要一个 picklable 对象作为参数
    app.run(port=12345)


class TestAccess(unittest.TestCase):

    def setUp(self):
        self.server = Process(target=start_server)
        self.server.start()

    def tearDown(self):
        self.server.terminate()

if __name__ == '__main__':
    unittest.main()
