from __future__ import unicode_literals


def refine_STATICS(original):
    original['GENERAL']['css']['files'] += [
        'users/users.css',
    ]
    return original
