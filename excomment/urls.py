# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'comments', views.CommentViewSet, base_name='comments')
api = [
    url(r'^', include(router.urls)),
    url(r'^comments/children/?$', views.ChildrenCommentsListView.as_view(), name='comment_children'),
    url(r'^comments/author/(?P<author>\d+)/?$', views.UserCommentsListView.as_view(), name='comment_author'),
]

urlpatterns = [
    url(r'^api/', include(api, namespace='api')),
    url(r'^comments/in/(?P<format>\w+)$', views.get_comments_in_format, name='comments_in_xml'),
]
