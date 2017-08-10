# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from version.models import Client


User = get_user_model()


# Admin Views


class AdminUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("<a href=\"../password/\">Change password</a>"))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'is_active', 'is_staff']

    def clean_password(self):
        return self.initial['password']


class AdminPasswordChangeForm(forms.Form):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password (again)"),
                                widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AdminPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["password1"])
        if commit:
            self.user.save()
        return self.user
        

# User Views


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Login'})
        self.fields['password'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'Password'})

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
       
        if username and password:
            try:
                user_obj = User.objects.get(username=username)
            except:
                raise forms.ValidationError("User with this username does not exist.")
            if not user_obj.check_password(password):
                raise forms.ValidationError("You passed invalid password.")
            if not user_obj.is_active:
                raise forms.ValidationError("User is not active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    client = forms.ModelChoiceField(
        label = 'Client',
        queryset = Client.objects.all(),
        widget = forms.Select(attrs={
            'class':'form-control',
        }),
        required = False,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'client']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Login *'})
        self.fields['password1'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'Password *'})
        self.fields['password2'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'Confirm password *'})
        self.fields['email'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'email',
            'placeholder': 'E-mail *'})
        self.fields['first_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'First name'})
        self.fields['last_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Last name'})

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords must match.")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        label = 'Client',
        queryset = Client.objects.all(),
        widget = forms.Select(attrs={
            'class':'form-control',
        }),
        required = False,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'client']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Login *'})
        self.fields['email'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'email',
            'placeholder': 'E-mail *'})
        self.fields['first_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'First name'})
        self.fields['last_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Last name'})
        self.fields['is_active'].widget = forms.CheckboxInput(attrs={
            'class': 'checkbox',
            'type': 'checkbox'})


class PasswordChangeForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['password'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'Password *'})
        self.fields['password1'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'New password *'})
        self.fields['password2'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'Confirm new password *'})

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError("You passed invalid password.")
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords must match.")
        return password2

    def save(self, commit=True):
        password = self.cleaned_data.get('password1')
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class PasswordResetForm(forms.Form):
    email = forms.EmailField()

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        try:
            user = User.objects.get(email=email)
        except:
            raise forms.ValidationError("User with this email does not exist.") 
        return super(PasswordResetForm, self).clean(*args, **kwargs)

    def reset_password(self, email):
        user_obj = User.objects.get(email=email)
        password = User.objects.make_random_password()
        user_obj.set_password(password)
        user_obj.save()
        return password

    def send_email(self):
        user_email = self.cleaned_data['email']
        new_password = self.reset_password(user_email)

        user = User.objects.get(email=user_email)
        subject = "Your Version System account new password"
        message = "<p>Hi <b>%s</b>!<br>\
                   You have reset your password.\
                   Here is your new password: <b>%s</b><br>\
                   Now you can log in and change it\
                   in your profile.</p>\
                   <p>Thanks,\
                   <br>Version System administration</p>" % (
                    user.username, new_password
                   )
        from_email = settings.DEFAULT_FROM_EMAIL
        new_email = send_mail(
            subject,
            message,
            from_email,
            [user_email],
            html_message=message,
            fail_silently=False
        )
        return user_email