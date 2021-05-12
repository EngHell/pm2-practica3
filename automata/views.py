from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.timezone import datetime
from django.views.generic import FormView, ListView, CreateView, UpdateView

from automata.forms import UploadFileForm, EditUploadForm
from automata.models import Uploads
from automata.parser.lib import StringStream, Parser


class Index(LoginRequiredMixin, ListView):
    template_name = 'automata/list.html'
    model = Uploads

    def get_queryset(self):
        return Uploads.objects.filter(user=self.request.user)


class EditUploadedFileFormView(LoginRequiredMixin, UpdateView):
    template_name = 'automata/edit.html'
    form_class = EditUploadForm
    model = Uploads

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        obj: Uploads = self.get_object()
        if not obj.user == request.user and not request.user.is_staff:
            return HttpResponseForbidden()
        return super(EditUploadedFileFormView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EditUploadedFileFormView, self).get_context_data(**kwargs)
        f = self.get_object().file.open('r')
        file_content = f.read()
        context['file_content'] = file_content
        s = StringStream(file_content)
        p = Parser(s)
        p.parse()
        context['parsed'] = p.parsed
        #context['file_content'].replace('\r\n', '\n').replace('\r', '\n').replace('\n', '\r\n')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('automata:editor', kwargs={'pk': self.get_object().id}))


class UploadFileFormView(LoginRequiredMixin, CreateView):
    template_name = 'automata/upload.html'
    form_class = UploadFileForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('automata:index'))


def delete(request: HttpRequest, pk: int):
    upload = get_object_or_404(Uploads, pk=pk)

    if not upload.user == request.user and not request.user.is_staff:
        return HttpResponseForbidden()

    upload.delete()

    return HttpResponseRedirect(reverse('automata:index'))
