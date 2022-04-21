import random
import json
import os.path

from django.conf import settings

from .parameters import ALPHABET_FOR_PROMOCODE


def create_promocode():
    return ''.join([random.choice(ALPHABET_FOR_PROMOCODE) for x in range(10)])


def search_promocode(code):
    if os.path.exists(settings.FILE_PATH):
        with open(settings.FILE_PATH, 'r') as f:
            coupons = json.load(f)
        for group in coupons:
            promocodes = group.get('promocodes')
            if promocodes is not None:
                for promocode in promocodes:
                    if promocode.get('code') == code:
                        return group['group_name']
    else:
        return False
