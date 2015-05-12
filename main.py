import tornado.ioloop
import tornado.web
from app_scaler.config import Config
from app_scaler.apis import GUI, ServerAppApi


application = tornado.web.Application([
                  (r"/", GUI),
                  (r"/api", ServerAppApi),
])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start() 
