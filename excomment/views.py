# -*- coding: utf-8 -*-

from django.http import StreamingHttpResponse, HttpResponseNotFound
from django.utils.translation import ugettext_lazy as _

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.filters import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission

from . import serializers
from . import format_serializers
from .models import Comment
from .filters import CommentFilter


class AuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, AuthorPermission)

    pagination_class = type('CommentPagination', (PageNumberPagination,), {'page_size': 20,
                                                                           'page_size_query_param': 'size'})
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('content_type', 'object_id')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            qs = qs.filter(parent__isnull=True)
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if Comment.objects.filter(parent_id=instance.id).exists():
            return Response(data={'errors': [_('Comment has children'), ]},
                            status=status.HTTP_400_BAD_REQUEST)
        instance._action_by = request.user
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        serializer.instance._action_by = self.request.user
        serializer.instance._old_body = serializer.instance.body
        serializer.save()


class ChildrenCommentsListView(generics.ListAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'content_type', 'object_id')

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        if self.request.GET.get('id'):
            qs = qs.get().get_descendants()
        return qs.order_by('parent', 'created')


class UserCommentsListView(generics.ListAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all().order_by('created')

    def get_queryset(self):
        return super().get_queryset().filter(author_id=self.kwargs['author'])


def get_comments_in_format(request, format='xml'):
    qs = Comment.objects.all().select_related('author', 'content_type')
    qs = CommentFilter(request.GET, qs).qs
    content, content_type = format_serializers.serialize(format, qs)
    if content is None:
        return HttpResponseNotFound()
    response = StreamingHttpResponse(content, content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename="comments.' + format + '"                                                                        b'
    return response


