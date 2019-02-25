from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        filter_result = User.objects.filter(username__exact=username)
        if not filter_result:
            raise forms.ValidationError('This username does not exist, Please check')
        else:
            return username