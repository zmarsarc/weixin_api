# -*- coding: utf-8 -*-

import unittest
from api import MessageType
from xml.etree.ElementTree import ParseError, ElementTree


class TestBasicMessage(unittest.TestCase):

    class subclass(MessageType.base_message):

        def __init__(self, serialized_xml=None):
            try:
                super(TestBasicMessage.subclass, self).__init__(serialized_xml)
            except TypeError:
                pass

            self.__setup_filed()
            if serialized_xml is not None:
                self.__import_tree(serialized_xml)
            else:
                self.__create_empty_tree()

        def __setup_filed(self):
            self._content = None

        def __import_tree(self, serialized_xml):
            self._content = self._xml.find('Content').text

        def __create_empty_tree(self):
            ElementTree.SubElement(self._xml, 'Content')

        def __str__(self):
            return 'text'

        @property
        def content(self):
            return self._content

        @content.setter
        def content(self, value):
            self._content = value
            self.__set_text('Content', value)

    def setUp(self):
        with open('./test/Sample/ValidXML.xml') as fp:
            self.valid = fp.read()

        with open('./test/Sample/InvalidXML.Broken.xml', 'r') as fp:
            self.invalid_broken = fp.read()

        with open('./test/Sample/InvalidXML.MissingToken.xml', 'r') as fp:
            self.invalid_missing = fp.read()

    def test_init(self):
        xml = MessageType.base_message(self.valid)

        expect = {'tousername': 'toUser',
                  'fromusername': 'fromUser',
                  'createtime': 1348831860,
                  'msgid': 1234567890123456}

        self.assertEqual(expect['tousername'], xml.to_user_name)
        self.assertEqual(expect['fromusername'], xml.from_user_name)
        self.assertEqual(expect['createtime'], xml.create_time)
        self.assertEqual(expect['msgid'], xml.msg_id)

    def test_init_failure(self):
        self.assertRaises(ParseError, MessageType.base_message, serialized_xml=self.invalid_broken)
        self.assertRaises(AttributeError, MessageType.base_message, serialized_xml=self.invalid_missing)

    def test_init_new(self):
        xml = MessageType.base_message()

        self.assertEqual(None, xml.to_user_name)
        self.assertEqual(None, xml.from_user_name)
        self.assertEqual(None, xml.create_time)
        self.assertEqual(None, xml.msg_id)

    def test_find_failure(self):
        xml = MessageType.base_message(self.valid)

        def read_value():
            return xml.content

        self.assertRaises(AttributeError, read_value)

    def test_set(self):
        xml = MessageType.base_message(self.valid)
        expect = 1000

        xml.msg_id = expect
        self.assertEqual(expect, xml.msg_id)

    def test_subclass(self):
        xml = self.subclass(self.valid)
        expect = {'tousername': 'toUser',
                  'fromusername': 'fromUser',
                  'createtime': 1348831860,
                  'content': 'this is a test',
                  'msgid': 1234567890123456}

        self.assertEqual(expect['tousername'], xml.to_user_name)
        self.assertEqual(expect['fromusername'], xml.from_user_name)
        self.assertEqual(expect['createtime'], xml.create_time)
        self.assertEqual(expect["msgid"], xml.msg_id)
        self.assertEqual(expect['content'], xml.content)

    def test_dump(self):
        xml = MessageType.base_message(self.valid)
        sub_xml = TestBasicMessage.subclass(self.valid)
        none_xml = MessageType.base_message()

        expect = {}
        with open('./test/Sample/ExpectXML.Basie.xml') as fp:
            expect['xml'] = fp.read()
        with open('./test/Sample/ExpectXML.Sub.xml') as fp:
            expect['sub'] = fp.read()
        with open('./test/Sample/ExpectXML.None.xml') as fp:
            expect['none'] = fp.read()

        self.assertEqual(expect['xml'], xml.dump())
        self.assertEqual(expect['sub'], sub_xml.dump())
        self.assertEqual(expect['none'], none_xml.dump())
