# -*- coding: utf-8 -*-

import unittest
import os
from api import Config


class TestFileConfiger(unittest.TestCase):

    def setUp(self):
        os.environ['WX_CONF_PATH'] = os.path.join(os.getcwd(), 'test\\Sample')
        self.configer = Config.FileConfig("sample.wxcfg")

    def test_get(self):
        self.assertEqual(None, self.configer.get('name', default=None))
        self.assertEqual(u"223", self.configer.get('id'))

    def test_set(self):
        self.assertRaises(Config.OptionNotExistError, self.configer.set, option='name', value='ttt')
        self.assertEqual(1, self.configer.set('id', '223'))

    def test_add(self):
        value = 'aaa'
        self.configer.add('foo', value)
        self.assertEqual(value, self.configer.get('foo'))

    def tearDown(self):
        os.unsetenv('WX_CONF_PATH')
