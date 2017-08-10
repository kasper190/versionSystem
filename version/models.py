# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _
import os
from re import search
from shutil import rmtree


def file_directory_path(instance, filename):
    return 'version_{0}/{1}'.format(instance.version.id, filename)


class Client(models.Model):
    client_name = models.CharField(max_length=100, unique=True)
    ein = models.CharField(_('EIN'), max_length=50, unique=True)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=15)
    street = models.CharField(max_length=150)
    country = models.CharField(max_length=80, default=settings.DEFAULT_COUNTRY)
    phone_number = models.CharField(max_length=15, blank=True)
    sec_level = models.PositiveSmallIntegerField(default=0)
    license_number = models.CharField(max_length=15)
    license_date = models.DateField(auto_now=True, auto_now_add=False)
    expiration_version_date = models.DateField(auto_now=False, auto_now_add=False)
    expiration_changes_date = models.DateField(auto_now=False, auto_now_add=False)

    def __unicode__(self):
        return self.client_name

    def get_address(self):
        return unicode(self.street + ', ' + self.zipcode + ' ' + self.city)


class Version(models.Model):
    version = models.CharField(max_length=15)
    version_date = models.DateField(auto_now=False, auto_now_add=False)
    description = models.TextField(blank=True)
    clients = models.ManyToManyField(Client, blank=True)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.version

    def save(self, *args, **kwargs):
        self.version = self.version.replace(',', '.')
        super(Version, self).save(*args, **kwargs)

    def get_clients(self):
        return self.clients.all()

    def get_files(self):
        return self.files.all()


class File(models.Model):
    filename = models.CharField(max_length=50, blank=True)
    file = models.FileField(upload_to=file_directory_path)
    version = models.ForeignKey(Version, related_name='files', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-version']

    def __unicode__(self):
        return self.filename

    def save(self, *args, **kwargs):
        super(File, self).save(*args, **kwargs)
        if not self.filename:
            new_filename = search(r'version_\d+/(.+)', self.file.name).group(1)
            file_obj = File.objects.filter(id=self.id).update(filename=new_filename)
            return file_obj


class Change(models.Model):
    CHANGE_TYPE_CHOICES = (
        (0, 'News'),
        (1, 'Bug'),
        (9, 'Release'),
    )
    change_type = models.PositiveSmallIntegerField(choices=CHANGE_TYPE_CHOICES, default=0)
    date = models.DateField(auto_now=False, auto_now_add=False)
    sec_level = models.PositiveSmallIntegerField(default=0)
    version = models.CharField(max_length=10)
    description = models.TextField()
    client = models.ForeignKey(Client, related_name='changes', null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return unicode(self.id)


class Loggs(models.Model):
    DB_TABLE_CHOICES = (
        ('version_file','version_file'),
    )
    logg_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='loggs')
    db_table = models.CharField(_('db_table'), max_length=50, choices=DB_TABLE_CHOICES)
    record_id = models.PositiveIntegerField(_('record_id'))

    class Meta:
        verbose_name = 'logg'
        verbose_name_plural = 'loggs'
        ordering = ['-id']


@receiver(pre_delete, sender=Version)
def all_files_delete(sender, instance, **kwargs):
    if os.path.isdir('media/version_%d/' % instance.id):
        rmtree('media/version_%d/' % instance.id)


@receiver(pre_delete, sender=File)
def file_delete(sender, instance, **kwargs):
    instance.file.delete(False)