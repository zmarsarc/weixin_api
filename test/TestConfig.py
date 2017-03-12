# -*- coding: utf-8 -*-

import unittest
import os
from api import Config
from ConfigParser import NoOptionError


class TestBasicConfiger(unittest.TestCase):

    class subclass(Config.FileConfig):
        def _define_section(self):
            return 'test'

    def setUp(self):
        self.sample = open('sample', 'w')
        self.sample.write('[test]\nid = 123\n')
        self.sample.flush()
        self.configer = self.subclass(self.sample.name)

    def test_open_file(self):
        self.assertRaises(IOError, Config.FileConfig, 'config.cfg')

    def test_undefined_section(self):
        self.assertRaises(NotImplementedError, Config.FileConfig, self.sample.name)

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

    def test_add(self):
        value = 'aaa'
        self.configer.add('foo', value)
        self.assertEqual(value, self.configer.foo)
        self.assertEqual(value, self.configer.get('foo'))

    def tearDown(self):
        self.sample.close()
        os.remove(self.sample.name)
