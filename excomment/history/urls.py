# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from . import views

api = [
    url(r'^comments/history/(?P<comment>(\d+|all))/?$', views.HistoryListView.as_view(), name='history'),
]

urlpatterns = [
    url(r'^api/', include(api)),
]
