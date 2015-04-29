from app_scaler.facades import *
from tornado.ioloop import PeriodicCallback
from tornado.gen import coroutine
import sys
from collections import defaultdict

class REM(PeriodicCallback):
    
    def __init__(self, config):
        super(REM, self).__init__(self.run, 20*1000)
        self.config = config
        self.stats_src = StatsFacade(config)
        self.vmgr = VManagerFacade(config)
        self.app_ctl = AppFacade(config)
        self.app_repo = AppRepoFacade(config)
        self.app_vms = defaultdict(list)
        self.free_pool = []
        self.instance = None

    

    @coroutine
    def __run_app(self, backend, vm):
        try:
            yield self.app_ctl.run(vm['Instances'][0]['PrivateIpAddress'], 'server.jar', 'ServerJIQ')
            vm['ScalerState'] = 'running'
            print("New virtual machine is available for backend {}".format(backend))
        except:
            print("Problem running app {}".format(backend))
            
    @coroutine
    def __stop_app(self, backend, vm):
        try:
            yield self.app_ctl.stop(vm['Instances'][0]['PrivateIpAddress'])
            vm['ScalerState'] = 'stopped'
            self.free_pool.append(vm)
            print("Instance of {} turned off".format(backend))
        except:
            print("Problem stopping app {}".format(backend))
            
    @coroutine
    def __register_app(self, backend, vm):
        try:
            yield self.app_ctl.register(backend, vm['Instances'][0]['PrivateIpAddress'], '8080')
            vm['ScalerState'] = 'ready'
            print("New app is available for backend {}".format(backend))
        except:
            print("Problem registering app {}".format(backend))
            
    @coroutine
    def __unregister_app(self, backend, vm):
        try:
            yield self.app_ctl.unregister(backend, vm['Instances'][0]['PrivateIpAddress'], '8080')
            vm['ScalerState'] = 'unregistered'
            print("Unregistered instance from backend {}".format(backend))
        except:
            print("Problem unregistering app {}".format(backend))

    def __clear_backends(self):

        for backend in self.app_vms:
            for vm in self.free_pool:
                if vm in self.app_vms[backend]:
                    self.app_vms[backend].remove(vm)

        if len(self.free_pool) > self.config['ec2']['max_spare_vms']:
            for i in range(len(self.free_pool) - self.config['ec2']['max_spare_vms']):
                vm = self.free_pool.pop()
                self.vmgr.destroy_vm(vm['Instances'][0]['InstanceId'])

    @coroutine
    def run(self):
        stats = yield self.stats_src.get_stats()
        print(stats)
        for backend in self.app_vms:
            for vm in self.app_vms[backend]:
                if vm['ScalerState'] == 'initialized':
                    stats[backend] += self.config['lb']['slots']    
                    yield self.__run_app(backend, vm)
                elif vm['ScalerState'] == 'running':
                    stats[backend] += self.config['lb']['slots']    
                    yield self.__register_app(backend, vm)
                elif vm['ScalerState'] == 'unregistered':
                    yield self.__stop_app(backend, vm)

        self.__clear_backends()

        for app in stats:
            if stats[app] <= 0:
                instance = None
                if len(self.free_pool) == 0:
                    instance = self.vmgr.create_vm()
                else:
                    instance = self.free_pool.pop()
                instance['ScalerState'] = 'initialized' 
                self.app_vms[app].append(instance)
                
            elif stats[app] > 2*self.config['lb']['slots']:
                for vm in self.app_vms[app]:
                    if vm['ScalerState'] == 'ready':
                        yield self.__unregister_app(app, vm)
                        break
