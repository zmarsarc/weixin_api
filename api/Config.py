# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser, NoOptionError
from abc import abstractmethod, ABCMeta

from .Logger import Logger


class OptionNotExistError(LookupError):
    def __init__(self, *args, **kwargs):
        super(OptionNotExistError, self).__init__(*args, **kwargs)
        self.option = kwargs.get('option')


class AbstractConfig(object):
    """提供配置数据接口"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, option, group=None, default=None):
        """
        从配置集中读取配置项
        :param option: str -> 指定配置项名称
        :param group: （可选）指定配置项所在的组
        :param default: （可选）未能成功读取配置时返回的值
        :return: str
        """
        pass

    @abstractmethod
    def set(self, option, value, group=None):
        """
        设置配置集中指定项的值
        :param option: str -> 指定配置项名称
        :param value: str -> 需要写入的值
        :param group: （可选）配置项所在的组
        :return: int -> 成功写入的项目数
        :raise: OptionNotExistError -> 指定的项目不存在
        """
        pass

    @abstractmethod
    def add(self, option, value, group=None):
        """
        在配置集中新建一个配置项
        如果指定的项目已经存在，则覆盖
        :param option: str -> 指定配置项目名称
        :param value: str -> 指定要配置的值
        :param group: （可选）str -> 配置项所在的配置组
        :return: int -> 成功设置的配置数
        """
        pass


class FileConfig(AbstractConfig):

    def __init__(self, filename):
        try:
            super(FileConfig, self).__init__(filename)
        except TypeError:
            super(FileConfig, self).__init__()

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
        try:
            fp = open(self.config_file, 'r')  # 如果找不到配置文件，将会抛出 IOError
        except IOError:
            Logger.get_logger().warn('config file \"%s\" not exist', self.config_file)
        fp.close()
        configer = ConfigParser()
        configer.read(self.config_file)
        return configer

    def _write_config_file(self):
        with open(self.config_file, 'w') as fp:
            Logger.get_logger().info("write config file \"%s\" in %s", self.config_file, self.__class__)
            self._configer.write(fp)

    def __setattr__(self, key, value):
        if not hasattr(self, '_limited'):
            self.__dict__['_limited'] = False
        if self._limited and key not in self.__dict__.keys():
            raise AttributeError('no such option ' + key)
        self.__dict__[key] = value


class app(FileConfig):

    def _define_section(self):
        return 'App'


class server(FileConfig):

    def _define_section(self):
        return 'Server'


class token(FileConfig):

    def _define_section(self):
        return 'Token'
