from app_scaler.facades import *
from tornado.ioloop import PeriodicCallback
from tornado.gen import coroutine
import sys

class REM(PeriodicCallback):
    
    def __init__(self, config):
        super(REM, self).__init__(self.run, 10*1000)
        self.stats_src = StatsFacade(config)
        self.vmgr = VManagerFacade(config)
        self.instance = None

    @coroutine
    def run(self):
        stats = yield self.stats_src.get_stats()
        print(stats)
        if self.instance is None:
            self.instance = self.vmgr.create_vm()
        vm_status = self.vmgr.check_vm(self.instance['Instances'][0]['InstanceId'])
        print(vm_status)
        if vm_status == 'running':
            self.vmgr.destroy_vm(self.instance['Instances'][0]['InstanceId'])
        elif vm_status == 'terminated':
            sys.exit(0)

