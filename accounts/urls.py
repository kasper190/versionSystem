from django.conf.urls import url
from .views import (
    # LoginView,
    # LogoutView,
    RegisterView,
    UserDetailView,
    UserListView,
    UserPasswordChangeView,
    UserPasswordChangeDoneView,
    UserPasswordResetView,
    UserPasswordResetDoneView,
    UserUpdateView,
)

urlpatterns = [
    # url(r'^login/$', LoginView.as_view(), name='login'),
    # url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^password_change/$', UserPasswordChangeView.as_view(), name='password-change'),
    url(r'^password-change/done/$', UserPasswordChangeDoneView.as_view(), name='password-change-done'),
    url(r'^password-reset/$', UserPasswordResetView.as_view(), name='password-reset'),
    url(r'^password-reset/done/$', UserPasswordResetDoneView.as_view(), name='password-reset-done'),
    url(r'^profile/$', UserDetailView.as_view(), name='user-detail'),
    url(r'^users/$', UserListView.as_view(), name='user-list'),
    url(r'^users/(?P<pk>\d+)/$', UserUpdateView.as_view(), name='user-update'),
]