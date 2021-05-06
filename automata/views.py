from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.utils.timezone import datetime
from django.views.generic import FormView, ListView

from automata.forms import UploadFileForm
from automata.models import Uploads


class Index(LoginRequiredMixin, ListView):
    template_name = 'automata/list.html'
    model = Uploads

    def get_queryset(self):
        return Uploads.objects.filter(user=self.request.user)


class UploadFileFormView(LoginRequiredMixin, FormView):
    template_name = 'automata/upload.html'
    form_class = UploadFileForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        upload = form.save()
        print(upload)
        return HttpResponseRedirect(reverse('automata:index'))


def handle_uploaded_file(f: UploadedFile, request: HttpRequest):
    with open(get_file_upload_file_name(f, request), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()


def get_file_upload_file_name(f: UploadedFile, request: HttpRequest) -> str:
    return f'uploads/automata/{request.user.id}/{datetime.now().timestamp()}.p2'
