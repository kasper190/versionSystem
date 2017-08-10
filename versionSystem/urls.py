from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
import django.views.static

from accounts.views import (
    LoginView,
    LogoutView,
)


urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^', include('version.urls', namespace='version')),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('version:version-list'), permanent=False)),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        url(r'^static/(.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
        url(r'^robots.txt', lambda x: HttpResponse("User-Agent: *\nDisallow: /", content_type="text/plain"), name="robots_file"),
    ]
