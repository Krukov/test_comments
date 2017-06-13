# -*- coding: utf-8 -*-

import random

from django.contrib.auth import get_user_model
from django.db import connection
from django.db.transaction import atomic
from rest_framework.authtoken.models import Token

from excomment.models import Comment

User = get_user_model()
USER_ID = 10


def create_tree(users, min_depth=100, min_nodes=10**4):
    depth = min_depth + random.randint(0, min_depth * 0.1)
    nodes = min_nodes + random.randint(0, min_nodes * 0.01)
    nodes_per_level = int(nodes / depth)

    content_object = users[USER_ID]
    roots = [Comment.objects.create(author=random.choice(users), body='text_{}'.format(i),
                                    content_object=content_object, pk=i)
             for i in range(nodes_per_level)]
    parents = roots
    counter = len(parents)

    while depth:
        parents = [Comment.objects.create(
            pk=counter + i, author=random.choice(users),
            body='answer_{}'.format(node.body),
            content_object=content_object,
            parent=node
        ) for i, node in enumerate(parents)]
        counter += len(parents)
        depth -= 1


def main(init=True):
    if not init and Comment.objects.exists():
        return
    cleanup()
    with atomic():
        users = [User.objects.create_user(id=i, username='user_{}'.format(i)) for i in range(100)]
        Token.objects.create(user=users[0], key='1234567890')
        create_tree(users)
    with connection.cursor() as cursor:
        cursor.execute("SELECT setval('excomment_comment_id_seq', (SELECT MAX(id) FROM excomment_comment)+1);")
        cursor.fetchall()
    print(Comment.objects.all().count())


def cleanup():
    Comment.objects.all().delete()
    Token.objects.all().delete()
    User.objects.all().delete()
