import tornado.web
from tornado.gen import coroutine
import tornado.ioloop
import os
from tornado import template
import redis
import pickle
from app_scaler.facades import AppRepoFacade, AppFacade
from app_scaler.config import Config

class GUI(tornado.web.RequestHandler):

    def get(self):
        loader = template.Loader("app_scaler/templates/")
        self.write(loader.load("index.html").generate())

class ServerAppApi(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        config = Config()
        repo = AppRepoFacade(config)
        app = AppFacade(config)
        db = redis.StrictRedis()        
        f_info = self.request.files['fileToUpload'][0]
        f_name = f_info['filename']
        java_class = self.get_argument("javaClass")
        backend = self.get_argument("backendName")
        db.set(backend, pickle.dumps([f_name, java_class]))
        repo.put(f_name, f_info['body'])
        yield app.simple_register(backend)

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


