# -*- coding: utf-8 -*-

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import CommentHistory
from ..models import Comment


@receiver(post_save, sender=Comment)
def comment_post_save(sender, instance, created, **kwargs):
    comment = instance
    action = CommentHistory.ACTIONS.MODIFICATION
    if created:
        action = CommentHistory.ACTIONS.CREATE
    CommentHistory.create(comment, action)


@receiver(post_delete, sender=Comment)
def comment_post_delete(sender, instance, **kwargs):
    comment = instance
    CommentHistory.create(comment, CommentHistory.ACTIONS.DELETE)