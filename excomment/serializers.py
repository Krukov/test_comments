# -*- coding: utf-8 -*-

from rest_framework import serializers

from excomment.models import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'body', 'author', 'created', 'content_type', 'object_id', 'parent')
        read_only_fields = ('id', 'author', 'created')
