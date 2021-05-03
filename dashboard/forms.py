from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import StudentGenre, Major

MyUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    genre = forms.ModelChoiceField(queryset=StudentGenre.objects.all(), required=True, label='Genero', empty_label='Selecciona tu genero')
    cui = forms.CharField(required=True, min_length=13, max_length=13)
    major = forms.ModelChoiceField(queryset=Major.objects.all(), required=True, label='Carrera', empty_label='Slecciona tu carrera')
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Repetir Contraseña"

    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ['email', 'username', 'cui', 'genre', 'major', 'password1', 'password2', ]

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            MyUser.objects.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError('duplicate_email')

    def clean_cui(self):
        cui: str = self.cleaned_data['cui']
        if cui.isdigit():
            return cui

        raise forms.ValidationError('cui must be numeric')


    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.genre = self.cleaned_data['genre']

        if commit:
            user.save()

        return user


class UserUpdateFrom(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    cui = forms.CharField(required=True, min_length=13, max_length=13)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    genre = forms.ModelChoiceField(queryset=StudentGenre.objects.all(), required=True, label='Genero')
    major = forms.ModelChoiceField(queryset=Major.objects.all(), required=True, label='Carrera')

    def __init__(self, *args, **kwargs):
        f = super(UserUpdateFrom, self).__init__(*args, **kwargs)

        self.fields['genre'].initial = self.instance.genre_id
        self.fields['major'].initial = self.instance.major_id


    def clean_cui(self):
        cui: str = self.cleaned_data['cui']
        if cui.isdigit():
            return cui

        raise forms.ValidationError('cui must be numeric')

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'cui', 'first_name', 'last_name','genre','major']

    def save(self, commit=True):
        user = super(UserUpdateFrom, self).save(commit=False)
        user.email = self.cleaned_data['email']
        #lsuser.genre = self.cleaned_data['genre']
        #user.major = self.cleaned_data['major']

        if commit:
            user.save()

        return user
