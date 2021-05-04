from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .forms import CustomUserCreationForm, UserUpdateFrom
from django.contrib.auth.backends import ModelBackend
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.decorators import login_required
from secrets import token_urlsafe
from .models import ValidationToken, CustomUser
from django.conf import settings

# Create your views here.
MyUser = get_user_model()


@login_required()
def update(request):
    args = {}
    if request.method == 'POST':
        form = UserUpdateFrom(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('update_profile'))
    else:
        form = UserUpdateFrom(instance=request.user)

    args['form'] = form

    return render(request, 'dashboard/update_profile.html', args)


@login_required()
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def profile(request, user):
    u = get_object_or_404(MyUser, username=user)

    return render(request, 'dashboard/profile.html', {'profile': u})


def home(request):
    return render(request, 'dashboard/home.html')


def activate(request, token):
    try:
        t = ValidationToken.objects.get(code=token)
        t.user.activated = True
        t.user.save()
    except ValidationToken.DoesNotExist:
        return HttpResponseNotFound('<h1> not found i said c:</h1>')

    return redirect(reverse('login'))


def register(request):
    # form = CustomUserCreationForm()
    args = {}
    if request.method == "GET":
        args['form'] = CustomUserCreationForm()
    elif request.method == 'POST':
        args['form'] = form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user, 'django.contrib.auth.backends.ModelBackend')
            txt_template = get_template('registration/registration_confirmation_email.txt')
            html_template = get_template('registration/registration_confirmation_email.html')

            token = token_urlsafe(32)
            tokenObject = ValidationToken(code=token, user=user)
            tokenObject.save()
            link = reverse('activate_profile', args=[tokenObject.code])
            context = {'username': user.username, 'link': link, 'default_domain':settings.DEFAULT_DOMAIN}

            subject, from_email, to = 'Email de confirmacion de registro', 'admin@practica1.test', user.email

            text_processed = txt_template.render(context)
            html_processed = html_template.render(context)

            msg = EmailMultiAlternatives(subject, text_processed, from_email, [to])
            msg.attach_alternative(html_processed, 'text/html')
            msg.send()

            return redirect(reverse('profile', kwargs={'user': user.username}))

    return render(
        request,
        'registration/register.html',
        args
    )
