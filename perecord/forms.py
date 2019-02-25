# coding: utf-8
from django import forms

from .models import *


class OverTimeForm(forms.ModelForm):
    class Meta:
        model = OverTime
        fields = ['name','s_time', 'e_time', 'overtime_hours', 'memo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            's_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'e_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'overtime_hours': forms.TextInput(attrs={'class': 'form-control'}),
            'memo': forms.Textarea(attrs={'class': 'form-control'}),
        }