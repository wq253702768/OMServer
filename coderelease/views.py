# coding: utf-8
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .tasks import *
from .models import AddProjectRecode, ReleaseEnv, ReleaseProjectType,ReleaseConfig,ReleaseHost
import json


@login_required(login_url='/')
def project_list(request):
    username = request.user.username
    project_obj = AddProjectRecode.objects.all().order_by('-id')
    return render(request,'coderelease/index.html',locals())


@csrf_exempt
@login_required(login_url='/')
def project_add(request):
    username = request.user.username
    env_all = ReleaseEnv.objects.all()
    pro_type_all = ReleaseProjectType.objects.all()

    pro_type = request.GET.get('pro_type','')
    if request.method == "POST":
        print (request.POST)
        project_name = request.POST.get('project_name','')
        pro_type = request.POST.get('pro_type','')
        domain = request.POST.get('domain', '')
        env = request.POST.get('env','')
        git_url = request.POST.get('git_address','')
        dev_principal = request.POST.get('dev_principal','')
        kwargs = request.POST.get('kwargs','')
        print (kwargs)
        if env:
            env_config_obj = ReleaseConfig.objects.filter(env_id=ReleaseEnv.objects.get(name=env).id)
            if env_config_obj:
                config_obj = ReleaseConfig.objects.get(env_id=ReleaseEnv.objects.get(name=env).id)
                jenkins_url = config_obj.jenkins_url
                jenkins_username = config_obj.jenkins_username
                jenkins_password = config_obj.jenkins_password
                branch = config_obj.branch_name
                jenkins_credentials_id = config_obj.jenkins_credentials_id
                docker_registry = config_obj.docker_registry_address
                api_server = config_obj.api_server_address
                namespace = config_obj.namespace
                redis_pass = config_obj.redis_password
                rabbit_pass = config_obj.rabbitmq_password

                # jenkins_api = JenkinsApi(jenkins_url=jenkins_url, jenkins_username=jenkins_username,
                #                          jenkins_password=jenkins_password,
                #                          pro_type=pro_type, project_name=project_name, env=env, git_url=git_url,
                #                          branch=branch,
                #                          jenkins_credentials_id=jenkins_credentials_id, docker_registry=docker_registry,
                #                          api_server=api_server, namespace=namespace, redis_password=redis_pass,
                #                          rabbitmq_password=rabbit_pass)

                env_host_obj = ReleaseHost.objects.filter(env_id=ReleaseEnv.objects.get(name=env).id,pro_type_id=ReleaseProjectType.objects.get(name=pro_type).id)
                if env_host_obj:
                    host_list = []
                    for i in env_host_obj.values_list():
                        print (i)
                        host_port_list = []
                        id,env_id,sn_id,ip,server_name,port,pro_type_id,default_kwargs,data_path = i
                        host_port_list.append(ip)
                        host_port_list.append(port)
                        host_port_list.append(server_name)
                        host_port_list.append(data_path)
                        host_list.append(host_port_list)

                    if not kwargs:
                        kwargs = default_kwargs
                    print(kwargs)
                    project_management_obj = AddProjectRecode()
                    project_management_obj.pro_name = project_name
                    project_management_obj.pro_type_id = ReleaseProjectType.objects.get(name=pro_type).id
                    project_management_obj.principal = dev_principal
                    project_management_obj.env_name_id = ReleaseEnv.objects.get(name=env).id
                    project_management_obj.domain = domain
                    project_management_obj.git_url = git_url
                    project_management_obj.branch = branch
                    project_management_obj.data_path = data_path
                    project_management_obj.host_list = host_list
                    project_management_obj.kwargs = kwargs

                    project_management_obj.jenkins_url = jenkins_url
                    project_management_obj.jenkins_username = jenkins_username
                    project_management_obj.jenkins_password = jenkins_password
                    project_management_obj.jenkins_credentials_id = jenkins_credentials_id
                    project_management_obj.docker_registry = docker_registry
                    project_management_obj.api_server = api_server
                    project_management_obj.namespace = namespace
                    project_management_obj.redis_pass = redis_pass
                    project_management_obj.rabbit_pass = rabbit_pass
                    project_management_obj.save()
                    return HttpResponse('项目添加成功')
                else:
                    return HttpResponse('检查环境主机信息是否存在')
            else:
                return HttpResponse('检查环境配置是否存在')

    return render(request, 'coderelease/project_add.html',locals())


@csrf_exempt
@login_required(login_url='/')
def project_edit(request,pro_id):
    '''
    编辑项目
    :param request:
    :return:
    '''
    username = request.user.username
    pro = AddProjectRecode.objects.get(id=pro_id)
    if request.method == 'POST':
        pro_form = AddProjectRecodeForm(request.POST, instance=pro)
        if pro_form.is_valid():
            pro_form.save()
            return HttpResponse('编辑成功')
        else:
            return HttpResponse('表单无效')
    else:
        pro_form = AddProjectRecodeForm(instance=pro)
        print (pro.pro_type)
        return render(request,'coderelease/project_edit.html',locals())


@login_required(login_url='/')
def project_detail(request,pro_id):
    '''
    查看项目
    :param request:
    :return:
    '''
    pro_obj = AddProjectRecode.objects.filter(id=pro_id)
    if pro_obj:
        pro = AddProjectRecode.objects.get(id=pro_id)
        host_list = eval(pro.host_list)
        return render(request, 'coderelease/project_detail.html', locals())
    else:
        return HttpResponse('无此项目数据!!')


@login_required(login_url='/')
def project_release(request):
    '''
    项目发布
    :param request:
    :param id: 项目ID
    :return:
    '''
    pro_id = request.GET.get('pro_id','')
    pro_obj = AddProjectRecode.objects.filter(id=pro_id)
    task_dict = {}
    if pro_obj:
        for data in pro_obj.values_list():
            id, pro_name, pro_type, principal, env_name, domain, git_url, branch, host_list, \
            data_path, kwargs, jenkins_url, jenkins_username, jenkins_password, jenkins_credentials_id, \
            docker_registry, api_server, namespace, redis_pass, rabbit_pass, release_status, c_time, u_time = data

            task = jenkins_api_task.delay(jenkins_url=jenkins_url, jenkins_username=jenkins_username, jenkins_password=jenkins_password,
                      pro_type=ReleaseProjectType.objects.get(id=pro_type).name, project_name=pro_name, env=ReleaseEnv.objects.get(id=env_name).name,
                                   git_url=git_url, branch=branch,
                      jenkins_credentials_id=jenkins_credentials_id, docker_registry=docker_registry,
                      api_server=api_server, namespace=namespace, redis_pass=redis_pass,
                                   rabbit_pass=rabbit_pass, kwargs=eval(kwargs), host_list=eval(host_list))
            task_dict['task_id'] = task.task_id
            task_dict['pro_id'] = pro_id
            if task.task_id:
                pro_obj = AddProjectRecode.objects.get(id=pro_id)
                pro_obj.release_status = '2'
                pro_obj.save()
        return HttpResponse(json.dumps({'data': task_dict}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'data': False}), content_type='application/json')


@login_required(login_url='/')
def task_celery_reslut(request):
    pro_id = request.GET.get('pro_id','')
    print (pro_id)
    task_id =request.GET.get('task_id','')
    task = jenkins_api_task.AsyncResult(task_id)
    print(task_id)
    print (task.state)
    if task.state in ['SUCCESS']:
        pro_obj = AddProjectRecode.objects.get(id = pro_id)
        pro_obj.release_status = '3'
        pro_obj.save()
    elif task.state in ['FAILED']:
        pro_obj = AddProjectRecode.objects.get(id = pro_id)
        pro_obj.release_status = '4'
        pro_obj.save()
    print(task.result)
    return HttpResponse(json.dumps({'status': task.state,'result':task.result}), content_type='application/json')


def test(request):
    print('before run')
    result = "ok"
    print("after run")
    return HttpResponse(result)


