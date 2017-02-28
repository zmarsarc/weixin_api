# -*- coding: utf-8 -*-

import unittest
import os
from api import Config
from ConfigParser import NoOptionError


class TestBasicConfiger(unittest.TestCase):

    class subclass(Config.basic_configer):
        def _define_section(self):
            return 'test'

    def setUp(self):
        self.sample = open('sample', 'w')
        self.sample.write('[test]\nid = 123\n')
        self.sample.flush()
        self.configer = self.subclass(self.sample.name)

    def test_open_file(self):
        self.assertRaises(IOError, Config.basic_configer, 'config.cfg')

    def test_undefined_section(self):
        self.assertRaises(NotImplementedError, Config.basic_configer, self.sample.name)

    def test_get(self):
        self.assertEqual(None, self.configer.get('name', None))
        self.assertRaises(AttributeError, lambda: self.configer.name)
        self.assertEqual('123', self.configer.get('id'))
        self.assertEqual('123', self.configer.id)

    def test_set(self):
        self.assertRaises(NoOptionError, self.configer.set, option='name', value='ttt')

        def testfunc():
            self.configer.xxx = 'test'
        self.assertRaises(AttributeError, testfunc)

    def tearDown(self):
        self.sample.close()
        os.remove(self.sample.name)
