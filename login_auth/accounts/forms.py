from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Please enter a valid email.',
        }
    )
    password = forms.CharField(
        min_length=6,
        error_messages={
            'required': 'Password is required.',
            'min_length': 'Password must be at least 6 characters.',
        }
    )


class RegisterForm(forms.Form):
    full_name = forms.CharField(
        min_length=3,
        max_length=150,
        error_messages={
            'required': 'Full name is required.',
            'min_length': 'Name must be at least 3 characters.',
        }
    )
    email = forms.EmailField(
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Please enter a valid email.',
        }
    )
    password = forms.CharField(
        min_length=6,
        error_messages={
            'required': 'Password is required.',
            'min_length': 'Password must be at least 6 characters.',
        }
    )
    confirm_password = forms.CharField(
        error_messages={
            'required': 'Please confirm your password.',
        }
    )
    terms = forms.BooleanField(
        error_messages={
            'required': 'You must agree to the terms.',
        }
    )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

        return cleaned_data
