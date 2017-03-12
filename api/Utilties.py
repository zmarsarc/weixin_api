# -*- coding: utf-8 -*-
from hashlib import sha1


def signature_checked(args):
    sorted_args = sorted(['zmarsarc', args['timestamp'], args['nonce']])
    local_signature = sha1(''.join(sorted_args)).hexdigest()
    return args['signature'] == local_signature


class Signleton(type):

    def __new__(cls, *args, **kwargs):
        obj = super(Signleton, cls).__new__(cls, *args, **kwargs)
        setattr(obj, "_{0}__instance".format(cls.__name__), None)
        return obj

    def __call__(self, *args, **kwargs):
        if not self.__instance:
            obj = self.__new__(self, *args, **kwargs)
            self.__instance = obj
        return self.__instance