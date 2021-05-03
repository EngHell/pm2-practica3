from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import StudentGenre, Profession

MyUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    genre = forms.ModelChoiceField(queryset=StudentGenre.objects.all(), required=True, label='Genero', empty_label='Selecciona tu genero')
    cui = forms.CharField(required=True, min_length=13, max_length=13)
    profession = forms.ModelChoiceField(queryset=Profession.objects.all(), required=True, label='Profesion', empty_label='Slecciona tu profesion')
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Repetir Contraseña"

    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ['email', 'username', 'cui', 'genre', 'profession', 'password1', 'password2', ]

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
    profession = forms.ModelChoiceField(queryset=Profession.objects.all(), required=True, label='Profesion')

    def __init__(self, *args, **kwargs):
        f = super(UserUpdateFrom, self).__init__(*args, **kwargs)

        self.fields['genre'].initial = self.instance.genre_id
        self.fields['profession'].initial = self.instance.profession_id


    def clean_cui(self):
        cui: str = self.cleaned_data['cui']
        if cui.isdigit():
            return cui

        raise forms.ValidationError('cui must be numeric')

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'cui', 'first_name', 'last_name', 'genre', 'profession']

    def save(self, commit=True):
        user = super(UserUpdateFrom, self).save(commit=False)
        user.email = self.cleaned_data['email']
        #lsuser.genre = self.cleaned_data['genre']
        #user.profession = self.cleaned_data['profession']

        if commit:
            user.save()

        return user
