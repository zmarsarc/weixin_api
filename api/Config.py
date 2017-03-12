# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser, NoSectionError, NoOptionError
from .Logger import Logger

class basic_configer(object):

    def __init__(self, filename):
        try:
            super(basic_configer, self).__init__(filename)
        except TypeError:
            super(basic_configer, self).__init__()

        self.config_file = filename
        self._configer = self._open_config_file()
        self._section = self._define_section()
        self._options = self._get_options()
        self.__class__.__slots__ = [name for name in self._options.keys()]
        self.__dict__.update(self._options)
        self._limited = True

    def get(self, option, default=None):
        return self.__dict__.get(option, default)

    def set(self, option, value):
        if not hasattr(self, option):
            raise NoOptionError(self._section, option)
        self.add(option, value)

    def add(self, option, value):
        self.__dict__[option] = value
        self._configer.set(self._section, option, value)
        self._write_config_file()

    def _define_section(self):
        raise NotImplementedError(__name__ + str(self.__class__) + 'not implemented')

    def _define_slots(self):
        raise NotImplementedError(__name__ + str(self.__class__) + ' _define_slots not implemented')

    def _get_options(self):
        return {name: value for (name, value) in self._configer.items(self._section)}

    def _open_config_file(self):
        fp = open(self.config_file, 'r')  # 如果找不到配置文件，将会抛出 IOError
        fp.close()
        configer = ConfigParser()
        configer.read(self.config_file)
        return configer

    def _write_config_file(self):
        with open(self.config_file, 'w') as fp:
            Logger.get_logger().info("write config file %s in %s", self.config_file, self.__class__)
            self._configer.write(fp)

    def __setattr__(self, key, value):
        if not hasattr(self, '_limited'):
            self.__dict__['_limited'] = False
        if self._limited and key not in self.__dict__.keys():
            raise AttributeError('no such option ' + key)
        self.__dict__[key] = value


class app(basic_configer):

    def _define_section(self):
        return 'App'


class server(basic_configer):

    def _define_section(self):
        return 'Server'


class token(basic_configer):

    def _define_section(self):
        return 'Token'
