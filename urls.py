from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from excomment import urls
from excomment.history import urls as history_urls

urlpatterns = [
    url(r'^', include(urls)),
    url(r'^', include(history_urls)),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^admin/', admin.site.urls),
    ]

    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
