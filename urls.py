from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from excomment import urls

urlpatterns = [
    url(r'^', include(urls)),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + [
        url(r'^admin/', admin.site.urls),
    ]

    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
