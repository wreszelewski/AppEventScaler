import tornado.web
import tornado.ioloop
import os

class ServerAppApi(object):

    def is_available(app):
        pass

    def run_app(app):
        pass

class RemoteAppApi(tornado.web.RequestHandler):

    def initialize(self, repo_facade):
        self.repo_facade = repo_facade

    def get(self, action, name, java_class):
       
        obj = self.app_repo.get(name)
        app_path = os.path.join('/tmp', 'apps', name) 
        with open(app_path, 'wb') as out:
            out.write(obj)
        command = 'sudo rund -cp {} {} &'.format(name, class)
        os.popen(command)

