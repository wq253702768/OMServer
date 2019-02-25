from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from coderelease.models import ReleaseEnv
from .models import PlatformManagement

# Create your views here.


@login_required(login_url='/')
def platform_list(request, env_name):
    '''
    get env info
    get env to platform
    '''
    username = request.user.username
    env_id = ReleaseEnv.objects.get(name=env_name).id
    print (env_id)
    platform_obj = PlatformManagement.objects.filter(env_id=env_id)
    print (platform_obj.values_list())
    return render(request, 'platmanagement/platform_list.html', locals())

