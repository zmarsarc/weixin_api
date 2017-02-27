# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser, NoSectionError, NoOptionError


class basic_configer(object):

    config_file_path = 'config.cfg'

    def __int__(self):
        try:
            super(basic_configer, self).__int__()
        except TypeError:
            pass

        self._section = self._define_secton()
        self.__dict__.update(self._get_options())

    def get(self, option, default=None):
        raise NotImplemented(__name__ + self.__class__ + 'not implemented')

    def set(self, option, value):
        raise NotImplemented(__name__ + self.__class__ + 'not implemented')

    def add(self, option, value):
        raise NotImplemented(__name__ + self.__class__ + 'not implemented')

    def _define_secton(self):
        raise NotImplemented(__name__ + self.__class__ + 'not implemented')

    def _get_options(self):
        configer = ConfigParser()
        configer.read(self.config_file_path)
        return {name: value for (name, value) in configer.items(self._define_secton())}
