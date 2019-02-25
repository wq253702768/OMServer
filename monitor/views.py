from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import json
from monitor.models import PodStatus
from coderelease.models import ReleaseEnv


@csrf_exempt
def report(request):
    '''
    获取监控数据
    :param request:
    :return:
    '''
    if request.method == "POST":
        monitor_data = request.POST.get('monitor_data')
        data = json.loads(monitor_data)
        if not data:
            return HttpResponse(" 没有数据 !")
        if not issubclass(dict,type(data)):
            return HttpResponse("数据必须为字典格式")
        # 收集到数据，开始进入插入数据库
        env_obj = ReleaseEnv.objects.get(name=data.get('env'))
        if env_obj:
            obj = PodStatus()
            obj.env_id = env_obj.id
            obj.pod_up = data.get('up')
            obj.pod_down = data.get('down')
            obj.save()
            print('已插入[%s]条数据: UP:[%s]条, DOWN:[%s]条' % ((len(data.get('up'))+len(data.get('down'))),len(data.get('up')),len(data.get('down'))))
            return HttpResponse("[{}] Upload Data, Total:[{}] pieces, Up:[{}] pieces, Down:[{}] pieces".format(data.get('env'),(len(data.get('up'))+len(data.get('down'))),len(data.get('up')),len(data.get('down'))))
        else:
            print('[%s]环境不存在，请检查环境是否存在' % data.get('env'))

    else:
        return HttpResponse("数据有问题，请检查数据格式是否正确")


@login_required(login_url='/')
def env_status_list(request):
    # 获取最后一条插入的数据。即最新的一条
    # 获取所有环境信息
    username = request.user.username
    env_obj = ReleaseEnv.objects.all()
    monitor_obj = []
    for env in env_obj:
        env_obj_list = []
        try:
            obj = PodStatus.objects.filter(env_id=env.id).last()
            print (obj)
            pod_down_len = len(eval(obj.pod_down))
            pod_up_len = len(eval(obj.pod_up))
            pod_down_percent = int((pod_down_len/(pod_down_len+pod_up_len))*100)
            # 0
            env_obj_list.append(env.name)
            # 1
            env_obj_list.append(env.id)
            # 2
            env_obj_list.append(env.memo)
            # 3
            env_obj_list.append(pod_down_percent)
            # 4
            env_obj_list.append(obj.c_time)
            monitor_obj.append(env_obj_list)
        except:
            print('[%s]: 环境暂无数据' % env.name)
    return render(request, 'montior/index.html', locals())


@login_required(login_url='/')
def env_status_detail(request,env_id):
    username = request.user.username
    env_obj = ReleaseEnv.objects.filter(id=env_id)
    if env_obj:
        obj = PodStatus.objects.filter(env_id = env_id)
        envs = ReleaseEnv.objects.get(id=env_id)
        current_up_pod = len(eval(obj.last().pod_up))
        current_down_pod = len(eval(obj.last().pod_down))
        current_total_pod = current_down_pod + current_up_pod
        current_time = obj.last().c_time

        # 获取当前最新的十条数据
        ten_monitor_data = PodStatus.objects.filter(env_id = env_id).values_list().order_by('-id')[0:10]
        # print (type(ten_monitor_data))
        # print (ten_monitor_data.count())
        ten_data_list = []
        for i in ten_monitor_data:
            i_list = []
            i_list.append(len(eval(i[2])) + len(eval(i[3])))
            i_list.append(len(eval(i[2])))
            i_list.append(len(eval(i[3])))
            i_list.append(i[4])
            ten_data_list.append(i_list)
        print (ten_data_list)
    return render(request,'montior/env_status_detail.html',locals())