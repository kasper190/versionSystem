# -*- coding: utf-8 -*-
from __future__ import unicode_literals
    
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (
    FormView,
    ListView,
    RedirectView,
)
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from .forms import (
    PasswordChangeForm,
    PasswordResetForm,
    UserCreationForm,
    UserLoginForm,
    UserUpdateForm,
)


User = get_user_model()


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('version:version-list')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    url = '/login/'
    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class RegisterView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:user-list')
    permission_required = ['accounts.is_moderator']

    def form_valid(self, form):
        user = form.save(commit=False)
        if not self.request.user.is_staff:
            user.client = self.request.user.client
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        return super(RegisterView, self).form_valid(form)

    def handle_no_permission(self):
        raise PermissionDenied


class UserDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(id=self.request.user.id)
        return context


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    permission_required = ['accounts.is_moderator']

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(client=self.request.user.client)

    def handle_no_permission(self):
        raise PermissionDenied


class UserPasswordChangeView(LoginRequiredMixin, FormView):
    form_class = PasswordChangeForm
    template_name = 'accounts/password-change.html'
    success_url = reverse_lazy('accounts:password-change-done')

    def get_form_kwargs(self):
        kwargs = super(UserPasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form): 
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super(UserPasswordChangeView, self).form_valid(form)


class UserPasswordChangeDoneView(TemplateView):
    template_name = 'accounts/password-change-done.html'


class UserPasswordResetView(FormView):
    form_class = PasswordResetForm
    template_name = 'accounts/password-reset.html'
    success_url = reverse_lazy('accounts:password-reset-done')

    def form_valid(self, form):
        form.send_email()
        return super(UserPasswordResetView, self).form_valid(form)


class UserPasswordResetDoneView(TemplateView):
    template_name = 'accounts/password-reset-done.html'


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_update.html'
    success_url = reverse_lazy('accounts:user-list')
    permission_required = ['accounts.is_moderator']

    def test_func(self):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        if self.request.user.is_superuser:
            return True
        elif User.objects.get(id=pk).client is not None:
            return User.objects.get(id=pk).client.id == self.request.user.client.id
        else:
            return False

    def handle_no_permission(self):
        raise PermissionDenied