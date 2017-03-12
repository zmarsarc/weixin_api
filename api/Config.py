# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta
from .Utilties import Signleton


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

    __metaclass__ = Signleton

    def __init__(self):
        super(FileConfig, self).__init__()

    def add(self, option, value, group=None):
        super(FileConfig, self).add(option, value, group)

    def get(self, option, group=None, default=None):
        super(FileConfig, self).get(option, group, default)

    def set(self, option, value, group=None):
        super(FileConfig, self).set(option, value, group)
