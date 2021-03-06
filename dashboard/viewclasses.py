from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template.loader import get_template
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from ipware import get_client_ip

from dashboard.views import send_token_email


class MyLoginView(LoginView):
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url(self.request.user)
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.get_user()
        print(user.email)
        if user.activated:
            login(self.request, user)
            self.send_login_attempt_email()
            return HttpResponseRedirect(self.get_success_url(user))

        send_token_email(user)
        return HttpResponseRedirect(reverse('login') + f'?needs_activation=True')

    def get_success_url(self, user=None):
        url = self.get_redirect_url()
        return url or resolve_url(reverse('profile', kwargs={'user': user.username}))

    def get_context_data(self, **kwargs):
        context = super(MyLoginView, self).get_context_data(**kwargs)
        activated = self.request.GET.get('activated', 'notfound')
        needs_activation = self.request.GET.get('needs_activation', 'notfound')
        old_code = self.request.GET.get('old_code', 'notfound')

        if not needs_activation == 'notfound':
            context['needs_activation'] = True
        if not old_code == 'notfound':
            context['old_code'] = True
        if not activated == 'notfound':
            context['activated'] = True

        return context

    def send_login_attempt_email(self):
        txt_template = get_template('dashboard/login_attemp_email.txt')
        html_template = get_template('dashboard/login_attemp_email.html')
        user = self.request.user
        ip, routable = get_client_ip(self.request)
        context = {'username': user.username, 'ip': ip}

        subject, from_email, to = 'Email de aviso de inicio de sesion', 'admin@practica1.test', user.email

        text_processed = txt_template.render(context)
        html_processed = html_template.render(context)

        msg = EmailMultiAlternatives(subject, text_processed, from_email, [to])
        msg.attach_alternative(html_processed, 'text/html')
        msg.send()
