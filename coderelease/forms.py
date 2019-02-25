# coding: utf-8
from django import forms

from .models import *


class AddProjectRecodeForm(forms.ModelForm):
    class Meta:
        model = AddProjectRecode
        fields = ['pro_name', 'pro_type', 'principal', 'env_name', 'domain', 'git_url','data_path', 'kwargs']
        widgets = {
            'pro_type': forms.Select(attrs= {'class': 'form-control'}),
            'domain': forms.TextInput(attrs={'class': 'form-control'}),
            'pro_name': forms.TextInput(attrs = {'class': 'form-control'}),
            'git_url': forms.TextInput(attrs={'class': 'form-control'}),
            'principal': forms.TextInput(attrs={'class': 'form-control'}),
            'env_name': forms.Select(attrs={'class': 'form-control'}),
            'kwargs': forms.Textarea(attrs={'class': 'form-control'}),
            'data_path': forms.TextInput(attrs={'class': 'form-control'}),

        }