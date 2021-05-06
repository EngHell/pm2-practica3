import re

from django import forms

from automata.models import Uploads


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

        try:
            o = Uploads.objects.get(user=self.user, name=name)
            raise forms.ValidationError('This file name already exists.')
        except Uploads.DoesNotExist:
            pass

        return name

    def clean_file(self):
        file = self.cleaned_data.get('file')
        print(file.name)
        if not re.match(r'.*\.p2$', file.name):
            raise forms.ValidationError('The file must have .p2 extension')

        return file

    def save(self, commit=True):
        upload = super(UploadFileForm, self).save(commit=False)

        if commit:
            upload.user = self.user
            upload.save()

        return upload
