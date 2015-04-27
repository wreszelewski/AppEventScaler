from app_scaler.facades import *
from tornado.ioloop import PeriodicCallback
from tornado.gen import coroutine
import sys

class REM(PeriodicCallback):
    
    def __init__(self, config):
        super(REM, self).__init__(self.run, 10*1000)
        self.stats_src = StatsFacade(config)
        self.vmgr = VManagerFacade(config)
        self.app_ctl = AppFacade(config)
        self.app_repo = AppRepoFacade(config) 
        self.instance = None

    @coroutine
    def run(self):
        stats = yield self.stats_src.get_stats()
        print(stats)
        #if self.instance is None:
        #    self.instance = self.vmgr.create_vm()
        #else:
        #    state = self.vmgr.check_vm(self.instance.id) 
        #    print(state)
        self.app_repo.put("test", "test")
        obj = self.app_repo.get("test")
        print(obj)
        yield self.app_ctl.register('tescik.localhost.com', '127.0.0.3', '80')
        if stats['tescik.localhost.com']>50:
            yield self.app_ctl.unregister('tescik.localhost.com', '127.0.0.3', '80')
    

