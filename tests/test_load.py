# -*- coding: utf-8 -*-

import os
import random
import time
from functools import wraps
from unittest import TestCase

import requests

HOST = os.environ.get('HOST', 'localhost:8080')
BASE = 'http://{}/api/comments/'.format(HOST)
USER_CT = 2
USER_ID = 10
REPEAT = 100
request_params = {'headers': {'Authorization': 'Token 1234567890'}}


def repeat(n):
    def decor(func):
        @wraps(func)
        def _test(*args, **kwargs):
            for i in range(n):
                func(*args, **kwargs)
        return _test
    return decor


class LoadTestCase(TestCase):

    @repeat(REPEAT)
    def test_create_comment_root(self):
        start = time.time()
        res = requests.post(BASE, json={'body': 'new comment', 'content_type': USER_CT, 'object_id': USER_ID},
                            **request_params)
        assert res.status_code == 201, res.content
        assert time.time() - start < 1.0

    @repeat(REPEAT)
    def test_create_comment_middle(self):
        start = time.time()
        res = requests.post(BASE, json={'body': 'new comment', 'content_type': USER_CT,
                                        'object_id': USER_ID, 'parent': random.randint(1, 10000)},
                            **request_params)
        assert res.status_code == 201, res.content
        assert time.time() - start < 1.0

    @repeat(REPEAT)
    def test_create_comment_last(self):
        start = time.time()
        res = requests.post(BASE, json={'body': 'new comment', 'content_type': USER_CT,
                                        'object_id': USER_ID, 'parent': random.randint(9000, 10000)},
                            **request_params)
        assert res.status_code == 201, res.content
        assert time.time() - start < 1.0

    @repeat(REPEAT)
    def test_get_root(self):
        start = time.time()
        res = requests.get(BASE, {'content_type': USER_CT, 'object_id': USER_ID, 'page': 5})
        assert res.status_code == 200, res.content
        assert res.json()['results'] != [], res.json()
        assert time.time() - start < 1.0

    @repeat(REPEAT)
    def test_get_for_user(self):
        start = time.time()
        res = requests.get(BASE + 'author/' + str(random.randint(1, 100)))
        assert res.status_code == 200
        assert time.time() - start < 1.0
