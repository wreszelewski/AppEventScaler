import tornado.ioloop
import tornado.web
from app_scaler.apis import RemoteAppApi

application = tornado.web.Application([
    (r"/", RemoteAppApi),
])

if __name__ = "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
