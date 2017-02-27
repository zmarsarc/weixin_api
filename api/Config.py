# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser, NoSectionError, NoOptionError


class basic_configer(object):

    config_file_path = 'config.cfg'

    def __int__(self):
        super(configer, self).__int__()

    def get(self, option, default=None):
        raise NotImplemented(__name__ + self.__class__ + 'not implemented')

    def set(self, option, value):
        raise NotImplemented(__name__ + self.__class__ + 'not implemented')

    def add(self, option, value):
        raise NotImplemented(__name__ + self.__class__ + 'not implemented')
