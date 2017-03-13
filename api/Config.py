# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta
from Utilties import Signleton
from Logger import Logger
import os
import sys


class OptionNotExistError(LookupError):
    def __init__(self, *args, **kwargs):
        super(OptionNotExistError, self).__init__(*args, **kwargs)
        self.option = kwargs.get('option')
        self.location = kwargs.get('location')
        self.message = 'No such option {0} in {1}'.format(self.option, self.location)


class ConfigFileNotExistError(EnvironmentError):
    def __init__(self, path, *args, **kwargs):
        super(ConfigFileNotExistError, self).__init__(*args, **kwargs)
        self.path = path
        self.message = 'can not find config {0}'.format(self.path)


class NoValidConfigFileError(EnvironmentError):
    def __init__(self, *args, **kwargs):
        super(NoValidConfigFileError, self).__init__(*args, **kwargs)
        self.message = 'no valid config neither default nor user specific'


class AbstractConfig(object):
    """提供配置数据接口"""
    # __metaclass__ = ABCMeta

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

    """
    文件搜索策略：
    1.首先搜索环境变量 WX_CONF_PATH 所指定的目录，如果有多个，则按照出现顺序搜素
    2.搜索与包同级的 conf 目录
    3.搜索本文件所在的目录

    配置导入策略：
    1.按照搜索策略找到配置文件则导入其内容
    2.如果没有找到用户指定的配置文件，则按照搜索策略查找 default.wxcfg
    3.若以上两项都失败，应当抛出 NoValidConfigFileError，在日志中写入 critical 错误，并且退出
    """
    __metaclass__ = Signleton

    def __init__(self, filename=None):
        super(FileConfig, self).__init__()

        self.logger = Logger.get_logger()
        self.filename = filename if filename is not None else 'default.wxcfg'
        try:
            self.fp = self.__open_config_file(self.filename)
        except NoValidConfigFileError:
            self.logger.fatal('no any config files available')
            sys.exit(1)
        else:
            self.logger.info('open config file %s', self.filename)

    def add(self, option, value, group=None):
        super(FileConfig, self).add(option, value, group)

    def get(self, option, group=None, default=None):
        super(FileConfig, self).get(option, group, default)

    def set(self, option, value, group=None):
        super(FileConfig, self).set(option, value, group)

    def __open_config_file(self, filename):
        try:
            return self.__open_user_config(filename)
        except ConfigFileNotExistError:
            return self.__open_default_config()

    def __open_default_config(self):
        paths = self.__generate_conf_file_path('default.wxcfg')
        for f in paths:
            try:
                return self.__open_file_with_read(f)
            except ConfigFileNotExistError:
                pass
        else:
            self.logger.warning('can not find any default config files')
            raise NoValidConfigFileError()

    def __open_user_config(self, filename):
        paths = self.__generate_conf_file_path(filename)
        for f in paths:
            try:
                return self.__open_file_with_read(f)
            except ConfigFileNotExistError:
                pass
        else:
            self.logger.warning('can not find any user config files')
            raise ConfigFileNotExistError(filename)

    def __open_file_with_read(self, filepath):
        try:
            return open(filepath, 'r')
        except IOError:
            self.logger.warning('config file %s not exist', filepath)
            raise ConfigFileNotExistError(filepath)

    def __generate_conf_file_path(self, filename):
        paths = []
        try:
            paths = [p for p in os.getenv('WX_CONF_PATH').split(';') if os.path.exists(p)]
        except AttributeError:
            self.logger.info('environment various WX_CONF_PATH not exist')
        # 将当前工作目录下的 conf 和 api 目录加入搜索列表
        # 这里假设工作目录下有 api 包并且 conf 和 api 包同级
        # TODO: 事实上这种假设是错误的
        paths.extend([os.path.join(os.getcwd(), p) for p in ('conf', 'api')])
        return [os.path.join(p, filename) for p in paths]
