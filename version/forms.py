# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from .models import (
    Change,
    Version,
)


class ContactForm(forms.Form):
    TOPIC_CHOICES = (
        (_("Version"), _("Version")),
        (_("Changes"), _("Changes")),
        (_("Other"), _("Other")),
    )
    topic = forms.ChoiceField(choices=TOPIC_CHOICES, widget=forms.Select(attrs={
        'id': 'topic',
        'class':'form-control form'})
    )
    topic_version = forms.ModelChoiceField(
        label = 'Choose version',
        queryset = Version.objects.all().values_list('id', flat=True),
        widget = forms.Select(attrs={
            'class':'form-control form topic_version',
        }),
        required = False,
    )
    topic_change = forms.CharField(required=False)
    topic_custom = forms.CharField(required=False)
    name = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['topic_change'].widget = forms.TextInput(attrs={
            'class': 'form-control form topic_change',
            'type': 'text',
            'placeholder': 'Change ID'})
        self.fields['topic_custom'].widget = forms.TextInput(attrs={
            'class': 'form-control form topic_custom',
            'type': 'text',
            'placeholder': 'Topic'})
        self.fields['name'].widget = forms.TextInput(attrs={
            'class': 'form-control form',
            'type': 'text',
            'placeholder': 'Name *'})
        self.fields['email'].widget = forms.TextInput(attrs={
            'class': 'form-control form',
            'type': 'email',
            'placeholder': 'E-mail *'})
        self.fields['phone_number'].widget = forms.TextInput(attrs={
            'class': 'form-control form',
            'type': 'text',
            'placeholder': 'Phone number'})
        self.fields['message'].widget = forms.Textarea(attrs={
            'class': 'form-control form textarea',
            'type': 'text',
            'contentEditable': 'true',
            'placeholder': 'Message *'})

    def send_email(self):
        msg_html = render_to_string('version/contact_email.html', {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'phone_number': self.cleaned_data['phone_number'],
            'topic': self.cleaned_data['topic'],
            'topic_version': self.cleaned_data['topic_version'],
            'topic_change': self.cleaned_data['topic_change'],
            'topic_custom': self.cleaned_data['topic_custom'],
            'message': self.cleaned_data['message'],
        })

        subject = "Version System: e-mail from " + self.cleaned_data['name']
        from_email = settings.DEFAULT_FROM_EMAIL
        to_mail = settings.EMAIL_TO
        new_email = send_mail(
            subject,
            msg_html,
            from_email,
            to_mail,
            html_message=msg_html,
            fail_silently=False
        )
        return subject