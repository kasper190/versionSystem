# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.core.signals import request_finished
from django.db.models import Q
from django.dispatch import receiver
from django.http import (
    Http404,
    HttpResponse,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    FormView,
    ListView,
    TemplateView,
)
import os
import operator
from re import match
from shutil import (
    make_archive, 
    rmtree,
)

from .forms import (
    ContactForm,
)
from .models import (
    Change,
    Client,
    File,
    Loggs,
    Version,
)


class ExpirationVersionMixin(UserPassesTestMixin):
    raise_exception = True
    permission_denied_message = 'Your license expired. In order to continue to use this \
                                functionality, please purchase a new license.'

    def test_func(self):
        if not self.request.user.is_staff:
            if not self.request.user.client is None:
                return self.request.user.client.expiration_version_date >= date.today()
            else:
                return False
        else:
            return True


class ExpirationChangesMixin(UserPassesTestMixin):
    raise_exception = True
    permission_denied_message = 'Your license expired. In order to continue to use this \
                                functionality, please purchase a new license.'
                                
    def test_func(self):
        if not self.request.user.is_staff:
            if not self.request.user.client is None:
                return self.request.user.client.expiration_changes_date >= date.today()
            else:
                return False
        else:
            return True


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'version/contact.html'
    success_url = reverse_lazy('version:contact-done')

    def get_initial(self):
        initial = super(ContactView, self).get_initial()
        if self.request.user.is_authenticated():
            first_name = self.request.user.first_name
            last_name = self.request.user.last_name
            if first_name and last_name:
                initial['name'] = first_name + ' ' + last_name
            initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)


class ContactDoneView(TemplateView):
    template_name = 'version/contact_done.html'


class ChangeList(LoginRequiredMixin, ExpirationChangesMixin, ListView):
    model = Change
    context_object_name = "changes"
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        change_obj = Change.objects.all()
        try:
            is_staff = self.request.user.is_staff
            if not is_staff:
                client_id = self.request.user.client.id
                client_obj = Client.objects.get(id=client_id)
                change_obj = change_obj.filter(
                    sec_level__lte = client_obj.sec_level
                )
        except:
            change_obj = change_obj.none()

        query = self.request.GET.get('q')
        if query:
            if match(r'^\d+,\d+$', query):
                query = query.replace(',', '.')
            query_list = query.split()
            change_obj = change_obj.filter(
                reduce(operator.or_,
                       (Q(id__contains=q) for q in query_list)) |
                reduce(operator.or_,
                       (Q(change_type__contains=q) for q in query_list)) |
                reduce(operator.or_,
                       (Q(date__icontains=q) for q in query_list)) |
                reduce(operator.or_,
                       (Q(version__icontains=q) for q in query_list)) |
                reduce(operator.or_,
                       (Q(description__icontains=q) for q in query_list)) |
                reduce(operator.or_,
                       (Q(client__client_name__icontains=q) for q in query_list))
            )

        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from or date_to:
            try:
                change_obj = change_obj.filter(
                    date__range = [date_from, date_to]
                )
            except:
                change_obj = change_obj.none()
        return change_obj

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['paginated_by'] = self.paginate_by
        query = self.request.GET.get('q')
        if query:
            context['q'] = query
        date_from = self.request.GET.get('date_from')
        if date_from:
            context['date_from'] = date_from
        date_to = self.request.GET.get('date_to')
        if date_to:
            context['date_to'] = date_to
        return context

    def get_paginate_by(self, queryset):
        pagination = self.request.COOKIES.get('change_paginated_by', '')
        if pagination:
            self.paginate_by = pagination
        return self.paginate_by


class VersionList(LoginRequiredMixin, ExpirationVersionMixin, ListView):
    model = Version
    context_object_name = "versions"
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        is_staff = self.request.user.is_staff
        if is_staff:
            version_obj = Version.objects.all()
        else:
            version_obj = Version.objects.filter(clients=self.request.user.client).all()

        ordering = self.request.GET.get('ordering', '-id')
        if ordering:
            version_obj = version_obj.order_by(ordering)
        
        query = self.request.GET.get('q')
        if query:
            if match(r'^\d+,\d+$', query):
                query = query.replace(',', '.')
            query_list = query.split()
            version_obj = version_obj.filter(
                reduce(operator.and_,
                       (Q(version__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list))
            )
        return version_obj
    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['paginated_by'] = self.paginate_by
        context['ordering'] = self.request.GET.get('ordering', '-id')
        query = self.request.GET.get('q')
        if query:
            context['q'] = self.request.GET.get('q')
        return context

    def get_paginate_by(self, queryset):
        pagination = self.request.COOKIES.get('version_paginated_by', '')
        if pagination:
            self.paginate_by = pagination
        return self.paginate_by


def file_download(request, pk):
    try:
        file = File.objects.get(id=pk)
        logger = Loggs(
            user = request.user,
            db_table = 'version_file',
            record_id = file.id,
        )
        logger.save()
    except File.DoesNotExist:
        raise Http404('File not found')
    return redirect(file.file.url)


class VersionFilesView(LoginRequiredMixin, ExpirationVersionMixin, View):
    @receiver(request_finished, sender=Version)
    def get(self, request, *args, **kwargs):
        version_id = self.kwargs['pk']
        
        dir_name = 'media/version_' + version_id
        output_filename = 'media/tmp/version_' + version_id
        make_archive(output_filename, 'zip', dir_name)
        file_path = output_filename + '.zip'
        zip_file = open(file_path, 'r')
        response = HttpResponse(zip_file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=version_%s.zip' % version_id

        for file_obj in File.objects.filter(version=version_id):
            logger = Loggs(
            user = request.user,
            db_table = 'version_file',
            record_id = file_obj.id,
            )
            logger.save()
        return response


@receiver(request_finished)
def zip_files(sender, **kwargs):
    if os.path.isdir('media/tmp/'):
        rmtree('media/tmp/')