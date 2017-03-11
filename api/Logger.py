# -*- coding: utf-8 -*-
import logging


class Logger(object):

    __isInit = False

    def __init__(self):
        filename = 'log/weixin.log'
        level = logging.DEBUG
        format = '%(asctime)s #%(levelname)s: %(message)s'
        logging.basicConfig(filename=filename, level=level, format=format)
        self.__isInit = True

    def get_logger(self):
        if not self.__isInit:
            self.__init__()
        return logging
