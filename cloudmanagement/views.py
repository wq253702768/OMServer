# coding: utf-8
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from coderelease.models import ReleaseEnv

def node_list(requst):
    return HttpResponse('ok')