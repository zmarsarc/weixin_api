# -*- coding: utf-8 -*-
from hashlib import sha1
from threading import Lock


def signature_checked(args):
    sorted_args = sorted(['zmarsarc', args['timestamp'], args['nonce']])
    local_signature = sha1(''.join(sorted_args)).hexdigest()
    return args['signature'] == local_signature


class Signleton(type):

    # TODO：当与 ABCMeta 一起使用时，如何拦截 ABCMeta 的请求？

    def __new__(cls, *args, **kwargs):
        obj = super(Signleton, cls).__new__(cls, *args, **kwargs)
        setattr(obj, "_{0}__instance".format(cls.__name__), None)
        setattr(obj, "_{0}__lock".format(cls.__name__), Lock())
        return obj

    def __call__(self, *args, **kwargs):
        if not self.__instance:
            self.__lock.acquire()
            if not self.__instance:
                obj = self.__new__(self, *args, **kwargs)
                obj.__init__(*args, **kwargs)
                self.__instance = obj
            self.__lock.release()
        return self.__instance