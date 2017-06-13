# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import CommentHistory


class HistorySerializer(serializers.ModelSerializer):
    action = serializers.CharField(source='get_action_display')

    class Meta:
        model = CommentHistory
        fields = ('id', 'when', 'who', 'comment', 'old_value', 'new_value', 'action')
