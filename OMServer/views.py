# coding: utf-8
from django.shortcuts import render,redirect,reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,Group
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

# Create your views here.
from monitor.models import PodStatus
from .forms import *
import random
import datetime


@csrf_exempt
def login_view(request):
    error = ''
    if request.method == 'GET':
        return render(request, 'login.html', locals())
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print (username,password)
        if username and password:
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('home_url'))
                else:
                    error = '用户未激活'
            else:
                error = '用户名或密码错误'
        else:
            error='用户名或密码错误'
    return render(request,'login.html',{'error': error})


@login_required(login_url='/')
def index(request):
    username = request.user.username
# get session online
    sessions = Session.objects.filter(expire_date__gte=datetime.datetime.now())
    uid_list = []

    # get session userid
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))
    online_sessions = User.objects.filter(id__in=uid_list)
    print(online_sessions)
    return render(request,'index.html',locals())


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login_url"))
def test1(request):
    return render(request,'test.html', locals())


@csrf_exempt
def test(request):
    i = random.randint(0,9)
    ret = []
    for n in range(0,i):
        result = PodStatus.objects.order_by("-id")[i].c_time
        ret.append(result)
    context = {"data": ret,}
    return JsonResponse(context)
