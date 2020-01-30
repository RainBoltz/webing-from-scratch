import tornado.ioloop
import tornado.web
import tornado.autoreload
import os, json
import random
import pandas as pd

version = 1
subversion = 0

# clean data
g_rawData = pd.read_csv('price_data.csv')
g_rawData = g_rawData[g_rawData['Volume'].map(lambda x: x > 0.0)]
g_rawData.drop('Volume', inplace=True, axis=1)
g_rawData.date = pd.to_datetime(g_rawData.date, format="%d.%m.%Y %H:%M:%S.000")
g_rawData.date = g_rawData.date.apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
g_fullData = g_rawData.to_json(orient='records')

class OHLCHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(g_fullData)

        
class MainWebpage(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
        

if __name__ == "__main__":
    application = tornado.web.Application(
    	handlers=[
            ("/api/v%d.%d/ohlc"%(version, subversion), OHLCHandler),
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
