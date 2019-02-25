# coding:utf-8
import os
import sys
import json
import shutil
from collections import namedtuple
from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
import ansible.constants as C
from .callback import PlaybookResultCallBack

C.HOST_KEY_CHECKING = False

Options = namedtuple('Options', [
    'listtags', 'listtasks', 'listhosts', 'syntax', 'connection',
    'module_path', 'forks', 'remote_user', 'private_key_file', 'timeout',
    'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
    'scp_extra_args', 'become', 'become_method', 'become_user',
    'verbosity', 'check', 'extra_vars', 'playbook_path', 'passwords',
    'diff', 'gathering', 'remote_tmp','ssh_args',
])


def get_default_options():
    options = Options(
        listtags=False,
        listtasks=False,
        listhosts=False,
        syntax=False,
        timeout=60,
        connection='ssh',
        module_path='',
        forks=10,
        remote_user='root',
        private_key_file=None,
        ssh_common_args="",
        ssh_extra_args="",
        sftp_extra_args="",
        scp_extra_args="",
        ssh_args="",
        become=None,
        become_method=None,
        become_user=None,
        verbosity=None,
        extra_vars=[],
        check=False,
        playbook_path='..',
        passwords=None,
        diff=False,
        gathering='implicit',
        remote_tmp='/tmp/.ansible'
    )
    return options


class PlayBookRunner:
    """
    用于执行AnsiblePlaybook的接口.简化Playbook对象的使用.
    """

    # Default results callback
    results_callback_class = PlaybookResultCallBack
    loader_class = DataLoader
    variable_manager_class = VariableManager
    options = get_default_options()

    def __init__(self,sources,playbook_file_path,options=None,passwords=None):
        '''

        :param sources: hosts file
        :param groups:  host_groups
        :param playbook_file_path: project + '/' + version + /' + envnamee + '.yml'
        :param options:
        '''
        if options:
            self.options = options
        C.RETRY_FILES_ENABLED = False
        self.sources = sources
        self.playbook_file_path = playbook_file_path
        self.loader = self.loader_class()
        self.results_callback = self.results_callback_class()
        self.inventory = InventoryManager(self.loader,sources=self.sources)
        self.variable_manager = self.variable_manager_class(
            loader=self.loader, inventory=self.inventory
        )
        self.passwords = passwords
        self.__check()
        self.run()

    def __check(self):
        if self.playbook_file_path is None or \
                not os.path.exists(self.playbook_file_path):
            raise AnsibleError(
                "Not Found the playbook file: {}.".format(self.playbook_file_path)
            )
        if not self.inventory.list_hosts('all'):
            raise AnsibleError('Inventory is empty')

    def run(self):
        try:
            executor = PlaybookExecutor(
                playbooks=[self.playbook_file_path],
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords
            )
            # if executor._tqm:
            #     executor._tqm._stdout_callback = self.results_callback
            executor._tqm._stdout_callback = self.results_callback
            executor.run()
            return self.results_callback
        finally:
            executor._tqm.cleanup()


if __name__ == "__main__":
    re = PlayBookRunner(sources=os.path.join('hosts'),playbook_file_path='task.yml')
    print (re.results_callback.output)
