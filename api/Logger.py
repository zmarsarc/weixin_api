# -*- coding: utf-8 -*-
import logging


class Logger(object):

    __isInit = False

    def __init__(self):
        filename = './log/weixin.log'
        level = logging.INFO
        format = '%(asctime)s #%(levelname)s: %(message)s'
        logging.basicConfig(filename=filename, level=level, format=format, filemode='w+')
        self.__isInit = True

    @staticmethod
    def get_logger():
        if not Logger.__isInit:
            Logger().__init__()
        return logging
