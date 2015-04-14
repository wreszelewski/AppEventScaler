import tornado.ioloop
import tornado.web
from app_scaler.rem import REM
from app_scaler.config import Config

class EventScalerApp(tornado.web.Application):

    def __init__(self, handlers=None, default_host="", transforms=None,
                 **settings):
        super(EventScalerApp, self).__init__(handlers, default_host, transforms)

        config = Config()
        main_thread = REM(config)
        main_thread.start()

application = EventScalerApp()

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start() 
