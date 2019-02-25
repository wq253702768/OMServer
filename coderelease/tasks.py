# -*- coding:utf-8 -*-
# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .api.ansible_api import PlayBookRunner
import sys
import os


@shared_task
def jenkins_api_task(jenkins_url, jenkins_username, jenkins_password,pro_type, project_name, env,
                     git_url, branch,jenkins_credentials_id, docker_registry=None,api_server=None, namespace=None,
                     redis_pass=None,rabbit_pass=None,kwargs=None, host_list=None):
    print (env)
    print (os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'env',env))
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'env',env))
    from release_api import JenkinsApi
    jenkins_api_obj = JenkinsApi(jenkins_url=jenkins_url, jenkins_username=jenkins_username, jenkins_password=jenkins_password,
                      pro_type=pro_type, project_name=project_name, env=env, git_url=git_url, branch=branch,
                      jenkins_credentials_id=jenkins_credentials_id, docker_registry=docker_registry,
                      api_server=api_server, namespace=namespace, redis_password=redis_pass,
                      rabbitmq_password=rabbit_pass)
    if pro_type in ['svc']:
        if not kwargs.get('mysql_user'):
            mysql_user = 'default'
        else:
            mysql_user = kwargs.get('mysql_user')

        if not kwargs.get('mysql_pass'):
            mysql_pass = 'default'
        else:
            mysql_pass = kwargs.get('mysql_pass')

        result = jenkins_api_obj.generate_svc_job(mysql_user=mysql_user, mysql_pass=mysql_pass)
        return result['message']
    elif pro_type in ['web']:
        if isinstance(kwargs, dict):
            if kwargs.get('release_dir_name'):
                release_dir_name = kwargs.get('release_dir_name')
            else:
                release_dir_name = 'dest'
            result = jenkins_api_obj.generate_web_job(release_dir_name=release_dir_name, host_list=host_list)
            print ('web',result)
            return result['message']

