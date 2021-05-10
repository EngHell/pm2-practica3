import re

from django import forms
from django.forms import Textarea
from automata.models import Uploads, get_file_upload_file_name


class UploadFileForm(forms.ModelForm):
    name = forms.CharField(max_length=500)
    file = forms.FileField()

    class Meta:
        model = Uploads
        fields = ['name', 'file']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not validate_file_extension(name):
            raise forms.ValidationError('Name should have a .p2 extension')

        try:
            o = Uploads.objects.get(user=self.user, name=name)
            raise forms.ValidationError('This file name already exists.')
        except Uploads.DoesNotExist:
            pass

        return name

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not validate_file_extension(file.name):
            raise forms.ValidationError('The file must have .p2 extension')

        return file

    def save(self, commit=True):
        upload = super(UploadFileForm, self).save(False)

        if commit:
            upload.user = self.user
            upload.save()

        return upload


class EditUploadForm(forms.ModelForm):
    name = forms.CharField(max_length=500)
    file = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Uploads
        fields = ['name', 'file']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EditUploadForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not validate_file_extension(name):
            raise forms.ValidationError('Name should have a .p2 extension')

        return name

    def clean_file(self):
        return self.data.get('file')

    def save(self, commit=True):
        upload: Uploads = self.instance

        if commit:
            upload.name = self.cleaned_data.get('name')
            upload.file = self.initial['file']
            handle_uploaded_file(self.cleaned_data.get('file'), upload.file.path)
            upload.save()

        return upload


def handle_uploaded_file(content: str, filepath: str):
    import os
    if os.path.exists(filepath):
        os.remove(filepath)

    with open(filepath, 'wt+') as destination:
        destination.write(content)

def validate_file_extension(name:str):
    return re.match(r'.*\.p2$', name)