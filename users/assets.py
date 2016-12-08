# coding=utf-8
from __future__ import unicode_literals, print_function

def refine_STATICS(original):

    original['GENERAL']['css']['files'] += [
        'users/users.css',
    ]

    return original
