# -*- coding: utf-8 -*-
from hashlib import sha1


def signature_checked(args):
    sorted_args = sorted(['zmarsarc', args['timestamp'], args['nonce']])
    local_signature = sha1(''.join(sorted_args)).hexdigest()
    return args['signature'] == local_signature
