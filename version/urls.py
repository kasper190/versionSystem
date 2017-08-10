from django.conf.urls import url
from .views import (
    ContactView,
    ContactDoneView,
    file_download,
    ChangeList,
    VersionFilesView,
    VersionList,
)

urlpatterns = [
    url(r'^changes/$', ChangeList.as_view(), name='change-list'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^contact/done/$', ContactDoneView.as_view(), name='contact-done'),
    url(r'^file/(?P<pk>\d+)/$', file_download, name='file-download'),
    url(r'^version/$', VersionList.as_view(), name='version-list'),
    url(r'^version/files/(?P<pk>\d+)/$', VersionFilesView.as_view(), name='version-files'),
]