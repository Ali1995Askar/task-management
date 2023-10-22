from users import forms
from django.contrib.auth import logout, login
from django.views import generic, View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from core.utils import anonymous_user_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView


@method_decorator(anonymous_user_required, name='dispatch')
class SignUpView(generic.CreateView):
    form_class = forms.SignupForm
    success_url = reverse_lazy("tasks:list")
    template_name = "users/signup.html"


@method_decorator(anonymous_user_required, name='dispatch')
class SignInView(LoginView):
    template_name = 'users/signin.html'
    form_class = forms.SigninForm


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(PasswordChangeView):
    form_class = forms.ChangePasswordForm
    template_name = 'users/change-password.html'
    success_url = reverse_lazy('users:signin')


@method_decorator(login_required, name='dispatch')
class SignOutView(View):
    template_name = 'users/sign-out.html'

    def get(self, request, *args, **kwargs):
        return render(request, f"{self.template_name}")

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(request)
            return redirect(reverse('users:signin'))
        else:
            return redirect(reverse('tasks:list'))
