# -*- coding: utf-8 -*-

from rest_framework import generics
from rest_framework.filters import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


from .serializers import HistorySerializer
from .models import CommentHistory


class HistoryListView(generics.ListAPIView):
    queryset = CommentHistory.objects.all().order_by('when')
    serializer_class = HistorySerializer
    pagination_class = type('HistoryPagination', (PageNumberPagination,), {'page_size': 10,
                                                                           'page_size_query_param': 'size'})

    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('when', 'action')

    def get_queryset(self):
        qs = super().get_queryset()
        if self.kwargs['comment'] == 'all':
            return qs
        return qs.filter(comment_id=self.kwargs['comment'])
