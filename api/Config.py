# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser, NoSectionError, NoOptionError


class basic_configer(object):

    config_file_path = 'config.cfg'

    def __int__(self):
        try:
            super(basic_configer, self).__int__()
        except TypeError:
            pass

        self._configer = self._open_config_file()
        self._section = self._define_secton()
        self._options = self._get_options()
        self.__dict__.update(self._options)

    def get(self, option, default=None):
        return self.__dict__.get(option, default)

    def set(self, option, value):
        if not hasattr(self, option):
            raise NoOptionError(self._section + 'has no option: ' + option)
        self.add(option, value)

    def add(self, option, value):
        self.__dict__[option] = value
        self._configer.set(self._section, option, value)
        self._write_config_file()

    def _define_secton(self):
        raise NotImplemented(__name__ + self.__class__ + 'not implemented')

    def _get_options(self):
        return {name: value for (name, value) in self._configer.items(self._section)}

    def _open_config_file(self):
        fp = open(self.config_file_path, 'r')  # 如果找不到配置文件，将会抛出 IOError
        fp.close()
        configer = ConfigParser()
        configer.read(self.config_file_path)
        return configer

    def _write_config_file(self):
        with open(self.config_file_path, 'w') as fp:
            self._configer.write(fp)
