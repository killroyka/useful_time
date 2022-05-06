from django.contrib import admin
from django.urls import include, path

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path("", include("homepage.urls"))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
