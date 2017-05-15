from django import forms

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Имя пользователя'),
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        label=_('Имя пользователя'),
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label=_('Адрес электронной почты'),
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=_('Enter your email')
    )

    password1 = forms.CharField(
        label='Пароль',
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            raise forms.ValidationError('Email already registered')
        except User.DoesNotExist:
            return email

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
