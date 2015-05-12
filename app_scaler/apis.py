import tornado.web
from tornado.gen import coroutine
from tornado import template
import redis
import json
from app_scaler.facades import AppRepoFacade
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
        db = redis.StrictRedis()        
        f_info = self.request.files['fileToUpload'][0]
        f_name = f_info['filename']
        java_class = self.get_argument("javaClass")
        backend = self.get_argument("backendName")
        db.hset(backend, 'app_info', json.dumps({'name': f_name, 'java_class': java_class}))
        repo.put(f_name, f_info['body'])

