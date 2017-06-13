# -*- coding: utf-8 -*-

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Comment(MPTTModel):
    _action_by = None  # for history
    _old_body = None  # for history

    body = models.TextField(max_length=255, verbose_name=_('Message'))
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE,
                               verbose_name=_('Author'))
    created = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id', 'created']),
            models.Index(fields=['parent']),
            models.Index(fields=['author', 'created']),
        ]
        ordering = ['created']

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return '{s.author} - {s.created} - {s.parent_id}'.format(s=self)
