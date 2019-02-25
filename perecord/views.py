from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from .models import OverTime
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .perecord_handler import date_calculation
from .forms import OverTimeForm
import json
import datetime


def index(request):
    return render(request, 'perecord/contacts.html', locals())


@login_required(login_url='/')
def overtime_list(request):
    username = request.user.username
    return render(request, 'perecord/overtime_list.html', locals())


@login_required(login_url='/')
def report_overtime_list(request):
    username = request.user.username
    print(username)
    print (request.GET)
    overtime_data = {
        "code":0,
        "msg":'',
        "count":'',
        "data":[],
    }
    overtime_list = OverTime.objects.filter(name=username).values_list()
    overtime_data['count'] = overtime_list.count()
    print(overtime_list.count())
    for data in overtime_list:
        table_data = {}
        id,name,s_time, e_time,overtime_hours, c_time, memo = data
        table_data['name'] = name
        table_data['s_time'] = s_time
        table_data['e_time'] = e_time
        table_data['overtime_hours'] = overtime_hours
        table_data['c_time'] = c_time.strftime('%Y-%m-%d %H:%M:%S')
        table_data['memo'] = memo
        overtime_data.get('data').append(table_data)
    print(overtime_data)
    return HttpResponse(json.dumps(overtime_data), content_type='application/json')


@login_required(login_url='/')
@csrf_exempt
def overtime_add(request):
    username = request.user.username
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        overtime_event = request.POST.get('overtime_event')
        overtime_hours = date_calculation(start_time,end_time)
        print ('dadadad',overtime_hours)
        if overtime_hours:
            try:
                overtime_obj = OverTime()
                overtime_obj.name = username
                overtime_obj.s_time = start_time
                overtime_obj.e_time = end_time
                overtime_obj.overtime_hours = overtime_hours
                overtime_obj.memo = overtime_event
                overtime_obj.save()
                return HttpResponse('success')
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse('falied')
    return render(request, 'perecord/overtime_add.html', locals())


@login_required(login_url='/')
@csrf_exempt
def overtime_delete(request,overtime_id):
    '''
    编辑项目
    :param request:
    :return:
    '''
    print (overtime_id)

    return render(request,'perecord/overtime_edit.html',locals())


def test(request):
    return render(request, 'perecord/test.html', locals())
