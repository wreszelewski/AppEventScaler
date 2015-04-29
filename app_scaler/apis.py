import tornado.web
import tornado.ioloop
import os
from tornado import template

class GUI(tornado.web.RequestHandler):

    def get(self):
        loader = template.Loader("app_scaler/templates/")
        self.write(loader.load("index.html").generate())

class ServerAppApi(object):

    def is_available(app):
        pass

    def run_app(app):
        pass

class RemoteAppApi(tornado.web.RequestHandler):

    def initialize(self, repo_facade):
        self.app_repo = repo_facade

    def get(self, *args, **kwargs):

        action = self.get_argument("action")
        name = self.get_argument("name")
        java_class = self.get_argument("java_class")
        if action=='start': 
            obj = self.app_repo.get(name)
            app_path = os.path.join('/tmp', 'apps', name) 
            with open(app_path, 'wb') as out:
                out.write(obj)
            command = 'sudo rund -cp {} {} &'.format(app_path, java_class)
            print(command)
            os.popen(command)
        elif action=='stop':
            command = 'killall dalvikvm'
            print(command)
            os.popen(command)


