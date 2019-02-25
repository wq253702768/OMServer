#!/usr/bin/env python
# coding: utf-8

from jenkinsapi import jenkins
import os
import sys
import importlib

importlib.reload(sys)


class JenkinsJobConfigXml(object):
    def __init__(self, project_name, jenkins_url, git_url, jenkins_credentials_id, branch, env, docker_registry=None,
                 api_server=None, redis_password=None, rabbitmq_password=None, namespace=None):
        '''

        :param project_name:
        :param jenkins_url:
        :param git_url:
        :param jenkins_credentials_id:
        :param branch:
        :param env:
        :param docker_registry:
        :param api_server:
        :param redis_password:
        :param rabbitmq_password:
        :param namespace:
        '''

        self.project_name = project_name
        self.env = env

        # jenkins info
        self.jenkins_url = jenkins_url
        self.git_url = git_url
        self.jenkins_credentials_id = jenkins_credentials_id
        self.branch = branch

        # docker info
        self.docker_registry = docker_registry

        # k8s info
        self.api_server = api_server
        self.namespace = namespace

        # business config info
        self.redis_password = redis_password
        self.rabbitmq_password = rabbitmq_password

    def svc_config_xml(self,mysql_user, mysql_pass):
        shell_context = '''#######请勿更改任何配置########
#######擅自更改者祭天！########
#####################################调整这一部分配置################################################
#项目名称
project_name="%s"
#项目名称,一般规定为项目名称的缩写
project_image_name="%s"
#mysql数据库用户
mysql_user="%s"
# mysql数据库密码
mysql_pass="%s"

#redis pass
redis_pass="%s"
# rabbit  pass
rabbit_pass="%s"
#############################################################基本不需要动的配置######################
#容器仓库地址
docker_registry="%s"
#环境slug,开发dev,测试test,预发布cn
env_slug="%s"
#api server地址
api_server="%s"
#namespace
namespace="%s"
#############################################################基本不需要动的配置####################

DATE=`date +%%Y%%m%%d`
jar_path=`find ${WORKSPACE}/target -name "*.jar"`
jar_name=`basename ${jar_path}`
docker_registry=${docker_registry}

docker_image_suffix=${project_image_name}

docker_image_v=$DATE-${BUILD_NUMBER}
docker_image_name="${docker_registry}/${docker_image_suffix}:${docker_image_v}"
k8s_deployment_dir="/data/k8s/${env_slug}/${project_name}"
k8s_deployment_yaml="${project_name}-deployment.yaml"


####下线设置####
################

###DB CONFIG###
###CONFIG DONE#

cp -f ${jar_path} ${WORKSPACE}


####build docker image and push...######
echo "#!/bin/sh
java -Xmx2g -jar ${jar_name} --spring.profiles.active=${env_slug} " > run.sh
chmod +x run.sh

cd ${WORKSPACE}

echo "##Dockerfile-jike###
FROM ${docker_registry}/fzjava:base
RUN mkdir -p /data/tomcat/project
ENV  LANG en_US.UTF-8
ENV  TZ Asia/Shanghai
ENV redis_pass ${redis_pass}
ENV rabbit_pass ${rabbit_pass}
ENV mysql_user ${mysql_user}
ENV mysql_pass ${mysql_pass}
ADD ${jar_name} /data/tomcat/project/${jar_name}
ADD run.sh /data/tomcat/project/run.sh
CMD [\&quot;/data/tomcat/project/run.sh\&quot;]&quot; &gt; Dockerfile

####push images####
echo "docker build -t ${docker_image_name}"
docker  build -t ${docker_image_name} .
docker  push ${docker_image_name}



#####k8s deployment service config files ############
cp -f ${k8s_deployment_dir}/${k8s_deployment_yaml}  ${WORKSPACE}
sed -i "s/jkk8sprojectimagetemp/${docker_registry}\/${docker_image_suffix}:${docker_image_v}/g" ${k8s_deployment_yaml}

/usr/local/bin/kubectl --server=${api_server} apply -f ${k8s_deployment_yaml}

###等待服务注册
sleep 300

###老服务从注册中心下线

for line in `cat ${project_name}.txt`
do
     echo $line
     kubectl --server=${api_server} --namespace=${namespace} exec $line curl  http://127.0.0.1:8080/rpc/org/rpc/rolling/app/delete?sleep=1000     
done

sleep 300

        ''' % (self.project_name, (self.project_name.replace("-", "")), mysql_user, mysql_pass,self.redis_password, self.rabbitmq_password,
               self.docker_registry, self.env, self.api_server, self.namespace)

        config_xml_context = '''
        <maven2-moduleset plugin="maven-plugin@3.1.2">
  <actions/>
  <description>111</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty plugin="gitlab-plugin@1.5.3">
      <gitLabConnection>jikeadmin</gitLabConnection>
    </com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty>
    <jenkins.model.BuildDiscarderProperty>
      <strategy class="hudson.tasks.LogRotator">
        <daysToKeep>-1</daysToKeep>
        <numToKeep>3</numToKeep>
        <artifactDaysToKeep>-1</artifactDaysToKeep>
        <artifactNumToKeep>-1</artifactNumToKeep>
      </strategy>
    </jenkins.model.BuildDiscarderProperty>
  </properties>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.8.0">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>%s</url>
        <credentialsId>%s</credentialsId>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>*/%s</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <goals>clean package -Dmaven.test.skip=true</goals>
  <aggregatorStyleBuild>true</aggregatorStyleBuild>
  <incrementalBuild>false</incrementalBuild>
  <ignoreUpstremChanges>false</ignoreUpstremChanges>
  <ignoreUnsuccessfulUpstreams>false</ignoreUnsuccessfulUpstreams>
  <archivingDisabled>false</archivingDisabled>
  <siteArchivingDisabled>false</siteArchivingDisabled>
  <fingerprintingDisabled>false</fingerprintingDisabled>
  <resolveDependencies>false</resolveDependencies>
  <processPlugins>false</processPlugins>
  <mavenValidationLevel>-1</mavenValidationLevel>
  <runHeadless>false</runHeadless>
  <disableTriggerDownstreamProjects>false</disableTriggerDownstreamProjects>
  <blockTriggerWhenBuilding>true</blockTriggerWhenBuilding>
  <settings class="jenkins.mvn.DefaultSettingsProvider"/>
  <globalSettings class="jenkins.mvn.DefaultGlobalSettingsProvider"/>
  <reporters/>
  <publishers>
    <com.ztbsuper.dingding.DingdingNotifier plugin="dingding-notifications@1.4">
      <accessToken>e4be8c941b442c7dea085c785e0c82e42fc0b2de78e9df30ddb4e22f485874c8</accessToken>
      <onStart>true</onStart>
      <onSuccess>true</onSuccess>
      <onFailed>true</onFailed>
      <jenkinsURL>%s</jenkinsURL>
    </com.ztbsuper.dingding.DingdingNotifier>
  </publishers>
  <buildWrappers/>
  <prebuilders/>
  <postbuilders>
    <hudson.tasks.Shell>
      <command>
      %s
      </command>
    </hudson.tasks.Shell>
  </postbuilders>
  <runPostStepsIfResult>
    <name>FAILURE</name>
    <ordinal>2</ordinal>
    <color>RED</color>
    <completeBuild>true</completeBuild>
  </runPostStepsIfResult>
</maven2-moduleset>
   ''' % (self.git_url, self.jenkins_credentials_id, self.branch, self.jenkins_url, shell_context)

        return config_xml_context

    def web_config_xml(self, release_dir_name, host_list):
        '''

        :param release_dir_name: web前端jenkins 下载的代码目录
        :param host_list: nginx前端列表
        :return:
        '''
        ansible_host_context = '''
        '''

        for host in host_list:
            ansible_host_context += "{} ansible_ssh_port={}\n".format(host[0], host[1])
        shell_context = '''
#############################################修改配置部分
#项目名称
project_name="%s"
#分支根下面的目录文件夹名称
release_dir_name="%s"
#环境标签，开发dev,测试test，预发布cn，生产com
env_slug="%s"
####################################################END
mv ${release_dir_name} ROOT
tar zcvf ROOT_${project_name}_${BUILD_NUMBER}.tar.gz ROOT &amp;&amp; rm -rf ROOT

cat &gt; hosts &lt;&lt; EOF
%s
EOF
remote_path=&quot;/data/tomcat/${env_slug}/app/${project_name}/webapps&quot;

cat &gt; deploy.yml &lt;&lt; EOF
- hosts: all
  remote_user: root
  tasks:
  - name: copy war to remote host
    copy: src=ROOT_${project_name}_${BUILD_NUMBER}.tar.gz dest=${remote_path} 
  - name: truncate project
    file: path=${remote_path}/ROOT/* state=absent
  - name: unzip teacher
    shell: cd ${remote_path} &amp;&amp; tar zxvf ROOT_${project_name}_${BUILD_NUMBER}.tar.gz  &amp;&amp; rm -rf  ROOT_${project_name}_${BUILD_NUMBER}.tar.gz
EOF

ansible-playbook -i hosts -v deploy.yml''' % (self.project_name, release_dir_name, self.env, ansible_host_context)

        config_xml_context = '''
<project>
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty plugin="gitlab-plugin@1.5.3">
      <gitLabConnection>jikeadmin</gitLabConnection>
    </com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty>
    <jenkins.model.BuildDiscarderProperty>
      <strategy class="hudson.tasks.LogRotator">
        <daysToKeep>-1</daysToKeep>
        <numToKeep>3</numToKeep>
        <artifactDaysToKeep>-1</artifactDaysToKeep>
        <artifactNumToKeep>-1</artifactNumToKeep>
      </strategy>
    </jenkins.model.BuildDiscarderProperty>
  </properties>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.8.0">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>%s</url>
        <credentialsId>%s</credentialsId>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>*/%s</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>
        %s</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>''' % (self.git_url, self.jenkins_credentials_id, self.branch, shell_context)
        return config_xml_context


class JenkinsApi(object):
    def __init__(self, jenkins_url, jenkins_username, jenkins_password, project_name, env, pro_type, git_url, branch,
                 jenkins_credentials_id, docker_registry=None, api_server=None, namespace=None, redis_password=None,
                 rabbitmq_password=None):
        '''

        :param projectname: 需要新增的项目名称
        :param env: 环境名称
        :param pro_type: 项目所属类型
        :param git_url: git地址拉取代码
        :param host_list: 主机列表
        '''

        # jenkins info
        self.jenkins_url = jenkins_url
        self.jenkins_username = jenkins_username
        self.jenkins_password = jenkins_password

        # other info
        self.project_name = project_name
        self.env = env
        self.pro_type = pro_type
        self.git_url = git_url
        self.branch = branch
        self.jenkins_credentials_id = jenkins_credentials_id
        self.docker_registry = docker_registry
        self.api_server = api_server
        self.namespace = namespace
        self.redis_password = redis_password
        self.rabbitmq_password = rabbitmq_password

        # instance
        self.server = self.login()

    def login(self):
        '''

        :return: jenkins login instance
        '''

        server = jenkins.Jenkins(self.jenkins_url, username=self.jenkins_username, password=self.jenkins_password)
        return server

    def is_job_exists(self):
        if self.server:
            try:
                self.server.get_job((self.env.upper() + "-" + self.pro_type + "-" + self.project_name))
                return True
            except Exception as e:
                return False

    def generate_web_job(self, release_dir_name, host_list):
        web_config_xml_data = JenkinsJobConfigXml(project_name=self.project_name,
                                                  env=self.env,
                                                  jenkins_url=self.jenkins_url,
                                                  git_url=self.git_url,
                                                  branch=self.branch,
                                                  jenkins_credentials_id=self.jenkins_credentials_id,
                                                  ).web_config_xml(release_dir_name=release_dir_name,
                                                                   host_list=host_list)

        if self.server:
            if self.is_job_exists():
                print('job is exists')
                message = 'job %s is exists' % (self.env.upper() + "-" + self.pro_type + "-" + self.project_name)
                return {'result': False,'message': message}
            else:
                try:
                    self.server.create_job((self.env.upper() + "-" + self.pro_type + "-" + self.project_name),
                                           web_config_xml_data.encode('UTF-8'))
                    print((self.env.upper() + "-" + self.pro_type + "-" + self.project_name))
                    message = '%s is create success' % (self.env.upper() + "-" + self.pro_type + "-" + self.project_name)
                    return {'result': True,'message': message}
                except jenkins.JenkinsAPIException as e:
                    message = e
                    return {'result': False,'message': message}

    def generate_svc_job(self,**kwargs):
        svc_config_xml_data = JenkinsJobConfigXml(project_name=self.project_name,
                                                  env=self.env,
                                                  jenkins_url=self.jenkins_url,
                                                  git_url=self.git_url,
                                                  docker_registry=self.docker_registry,
                                                  api_server=self.api_server,
                                                  namespace=self.namespace,
                                                  branch=self.branch,
                                                  redis_password=self.redis_password,
                                                  rabbitmq_password=self.rabbitmq_password,
                                                  jenkins_credentials_id=self.jenkins_credentials_id
                                                  ).svc_config_xml(mysql_user=kwargs.get('mysql_user'), mysql_pass=kwargs.get('mysql_pass'))
        if self.server:
            if self.is_job_exists():
                print('job is exists')
                message = 'job %s is exists' % (self.env.upper() + "-" + self.pro_type + "-" + self.project_name)
                return {'result': False,'message': message}

            else:
                try:
                        self.server.create_job((self.env.upper() + "-" + self.pro_type + "-" + self.project_name),
                                               svc_config_xml_data.encode('UTF-8'))
                        message = '%s creates success' % (self.env.upper() + "-" + self.pro_type + "-" + self.project_name)
                        return {'result': True, 'message': message}
                except jenkins.JenkinsAPIException as e:
                    message = e
                    return {'result': False, 'message':message}


if __name__ == "__main__":
    jenkins_url = 'http://192.168.97.70:8080'
    jenkins_username = 'admin'
    jenkins_password = 'OUpp2uQbf4rYSe4Q'
    project_name = 'bc-tal-web-wenqi'
    env = 'test'
    pro_type = 'web'
    git_url = 'http://gitlab.fclassroom.cn/fclassroom-visualizaiton/bc-tal.git'
    branch = 'test'
    jenkins_credentials_id = '34b28ce8-b816-4c9e-bb3d-de96b7427663'
    docker_registry = '192.168.97.70:5005'
    api_server = 'http://192.168.100.101:8080'
    namespace = 'jike-test'
    redis_password = 'RaBTIPq93pKoGPfT4h6C'
    rabbitmq_password = '34b28ce8-b816-4c9e-bb3d-de96b7427663'
    japi = JenkinsApi(jenkins_url=jenkins_url, jenkins_username=jenkins_username, jenkins_password=jenkins_password,
                      pro_type=pro_type, project_name=project_name, env=env, git_url=git_url, branch=branch,
                      jenkins_credentials_id=jenkins_credentials_id, docker_registry=docker_registry,
                      api_server=api_server, namespace=namespace, redis_password=redis_password,
                      rabbitmq_password=rabbitmq_password)
    # svc_api=japi.generate_svc_job()
    web_api=japi.generate_web_job(release_dir_name='test', host_list=[["192.168.100.100", 22], ["192.168.100.102", 22]])
    # print (svc_api)
    print(web_api)