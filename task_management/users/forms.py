from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import UsernameField, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, password_validation

User = get_user_model()


class SignupForm(auth_forms.UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', "autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'type': 'text',
                                                 'required': True,
                                                 'name': 'first_name',
                                                 'id': 'first_name'}),

            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'type': 'text',
                                                'required': True,
                                                'name': 'last_name',
                                                'id': 'last_name'}),

            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'type': 'email',
                                             'required': True,
                                             'name': 'email',
                                             'id': 'email'}),

            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'type': 'text',
                                               'name': 'username',
                                               'id': 'username'}),

        }


class SigninForm(auth_forms.AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                           "autofocus": True,
                                                           'type': 'username',
                                                           'name': 'username',
                                                           'id': 'username', }))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'type': 'password',
                                          'name': 'password',
                                          'id': 'password'}),
    )


class ChangePasswordForm(PasswordChangeForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        self.fields['old_password'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 'old_password',
            'id': 'old_password',
        })

        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 'new_password1',
            'id': 'new_password1',
            'help_text': password_validation.password_validators_help_text_html(),
        })

        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 'new_password2',
            'id': 'new_password2',
        })
