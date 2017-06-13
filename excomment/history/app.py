# -*- coding: utf-8 -*-

from django.apps import AppConfig


class HistoryAppConfig(AppConfig):
    name = 'excomment.history'

    def ready(self):
        from . import signals