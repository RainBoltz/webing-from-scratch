import tornado.ioloop
import tornado.web
import tornado.autoreload
import os, json
import random

version = 1
subversion = 1

class msgHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            param = self.get_argument("name", None)
            
            if param:
                message = "Hello, %s!"%param
            else:
                message = "Hello!!!"
                
            output = { "msg": message }
            self.write(json.dumps(output))
            
        except:
            self.set_status(500)
            
            
class MainWebpage(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
        

if __name__ == "__main__":
    application = tornado.web.Application(
    	handlers=[
            ("/api/v%d.%d/getMessage"%(version, subversion), msgHandler),
            (r"/", MainWebpage)
        ],
    	template_path=os.path.dirname(__file__),
    	static_path=os.path.join(os.path.dirname(__file__), "assets"),
        debug=True
    )
    
    the_port = 8888
    print('listen on port: %d'%the_port)
    
    application.listen(the_port)
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()