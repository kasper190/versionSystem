# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from version.models import Client


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    client = models.ForeignKey(Client, related_name='users', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        permissions = (
            ("is_moderator", "is moderator"),
        )