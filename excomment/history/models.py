# -*- coding: utf-8 -*-

import difflib
from urllib.parse import unquote_plus, quote_plus


from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..models import Comment

User = get_user_model()


class CommentHistory(models.Model):
    class ACTIONS:
        CREATE, MODIFICATION, DELETE = 0, 1, 2
        CHOICES = (
            (CREATE, _('Create')),
            (MODIFICATION, _('Modification')),
            (DELETE, _('Delete')),
        )

    when = models.DateTimeField(auto_now_add=True, db_index=True)
    who = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name=_('User'))

    comment = models.ForeignKey(Comment, related_name='history', null=True,
                                on_delete=models.SET_NULL, verbose_name=_('Comment'), db_index=True)
    diff = models.TextField(max_length=511, null=True, verbose_name=_('Encode Differ'))
    action = models.PositiveSmallIntegerField(choices=ACTIONS.CHOICES)

    @classmethod
    def create(cls, comment, action):
        fields = {'who': comment._action_by or comment.author, 'action': action, 'comment': comment}
        if action == cls.ACTIONS.MODIFICATION:
            fields['comment'] = comment
            if comment._old_body:
                fields['diff'] = cls.encode_diff(comment._old_body, comment.body)
        cls.objects.create(**fields)

    @staticmethod
    def encode_diff(old, new):
        diff = list(difflib.ndiff(old, new))
        if any((i.startswith(('+', '-')) for i in diff)):
            return ';'.join((quote_plus(i) for i in diff))

    @staticmethod
    def decode_diff(diff):
        return [unquote_plus(i) for i in diff.split(';')]

    def restore(self, new=False):
        return ''.join(difflib.restore(self.decode_diff(self.diff), int(new) + 1))

    @property
    def old_value(self):
        return self.restore(False)

    @property
    def new_value(self):
        return self.restore(True)
