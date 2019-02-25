# ~*~ coding: utf-8 ~*~
import os,sys
from PublishingPlatform.LoggingTemplate import Logging
from .ansible_api import PlayBookRunner


class AnsibleDataProcessing(object):
    def __init__(self,platform_id,env_id,module_name,action):
        self.action = action
        self.platform_id = platform_id
        self.env_id = env_id
        self.module_name = module_name
        self.platform_slug = Platform.objects.get(id=platform_id).slug
        self.env = Env.objects.get(id=env_id).name
        self.sources = os.path.join(settings.VARS_PATH,self.action ,self.platform_slug, self.env, 'hosts')
        self.playbook_file_path = os.path.join(settings.ROLES_PATH,self.action,self.platform_slug, self.env ,'%s.yml' % self.module_name)
        print ('file_path',self.playbook_file_path)
        print ('source======================',self.sources,self.playbook_file_path)
        self.result = PlayBookRunner(sources=self.sources,playbook_file_path = self.playbook_file_path).results_callback.output

    def check_task_stats(self):
        class_name = self.platform_slug + '-'+'AnsibleDataProcessing' + '-'+'check_task_stats'
        task_result = {}
        if self.result:
            for task_play in self.result['plays']:
                for index, task_info in enumerate(task_play['tasks']):
                    for hosts in task_info['hosts'].keys():
                        try:
                            if 'unreachable' in task_info['hosts'][hosts].keys():
                                result = Logging(level='error', msg='[%s] [%s] msg:[%s]' % (
                                        hosts, task_info['task']['name'], task_info['hosts'][hosts]['msg']),
                                        class_name=class_name).handle()
                                task_result[hosts] = result
                            elif 'changed' in task_info['hosts'][hosts].keys() and 'failed' in task_info['hosts'][hosts].keys():
                                if task_info['hosts'][hosts]['failed']:
                                    result = Logging(level='error', msg='[%s] [%s] msg:[%s]' % ( hosts, task_info['task']['name'], task_info['hosts'][hosts]['msg']),
                                            class_name=class_name).handle()
                                    task_result[hosts] = result
                            else:
                                if 'failed' in task_info['hosts'][hosts].keys():
                                    result = Logging(level='error', msg='[%s] [%s] msg:[%s]' % ( hosts, task_info['task']['name'], task_info['hosts'][hosts]['msg']),
                                            class_name=class_name).handle()
                                    task_result[hosts] = result
                        except KeyError:
                            pass
        print ('ansible error',task_result)
        self.play_stats_result = self.result['stats']
        task_hosts_f_dict = {}
        for hosts in self.play_stats_result.keys():
            if self.play_stats_result[hosts]['unreachable'] >0 or self.play_stats_result[hosts]['failures'] >0:
                task_hosts_f_dict[hosts] = task_result[hosts]
            else:
                task_hosts_f_dict[hosts] = 'ok'
        return task_hosts_f_dict


if __name__ == "__main__":
    import os
    from datetime import datetime
    platform_slug = 'coco'
    env = 'test'
    platform_id = 1
    env_id = 3
    for module_name in ['cocoDispatchServer']:
        print ('[%s] Start Release :[%s]' % (datetime.now(),module_name))
        re = AnsibleDataProcessing(platform_id=platform_id,env_id=env_id,module_name=module_name)
        print (re)
        print ('[%s] Over Release :[%s]' % (datetime.now(),module_name))

