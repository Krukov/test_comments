# -*- coding: utf-8 -*-

import django_filters
from django.db import models

from .models import Comment


class DateFilter(django_filters.DateTimeFilter):

    def filter(self, qs, value):
        if self.lookup_type == 'lte':
            value = value.replace(hour=23, minute=59, second=59)
        return super(DateFilter, self).filter(qs, value)


class CommentFilter(django_filters.FilterSet):
    filter_overrides = {models.DateTimeField: {'filter_class': DateFilter}}

    class Meta:
        model = Comment
        fields = {
            'created': ['lte', 'gte'],
            'author': ['exact'],
            'object_id': ['exact'],
            'content_type': ['exact'],
        }
