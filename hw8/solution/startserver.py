import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.escape import json_encode, json_decode
import os, json
import random
import pandas as pd

version = 1
subversion = 0

PASSWORD = "112233"

# clean data
g_rawData = pd.read_csv('price_data.csv')
g_rawData = g_rawData[g_rawData['Volume'].map(lambda x: x > 0.0)]
g_rawData.drop('Volume', inplace=True, axis=1)
g_rawData.date = pd.to_datetime(g_rawData.date, format="%d.%m.%Y %H:%M:%S.000")
g_rawData.date = g_rawData.date.apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

class OHLCHandler(tornado.web.RequestHandler):
    def post(self):
        #try:
        pw = self.get_argument("pw", None)
        outputData = None
        print("got password:", pw)
        
        if not pw:
            self.write("<script>alert(\"please input the password!\"); window.location.href = \"/\";</script>");
        elif pw != PASSWORD:
            self.write("<script>alert(\"wrong password!\"); window.location.href = \"/\";</script>");
        elif pw == PASSWORD:
            dstart = self.get_argument("dstart", '1900-01-01 00:00:00')
            dend = self.get_argument("dend", '2100-12-31 23:59:59')
            print("%s ~ %s"%(dstart, dend))
            rawData = g_rawData[(dstart <= g_rawData.date) & (g_rawData.date <= dend)]
            outputData = rawData.to_json(orient='records')
            self.render('candlestick.html', price_data=outputData)
        else:
            self.set_status(405)
            self.write("<script>alert(\"unknown error occurs!\"); window.location.href = \"/\";</script>");
            
        #except:
        #    self.set_status(500)
        
    def get(self):
        self.write("<script>alert(\"please input the password!\"); window.location.href = \"/\";</script>");

        
class MainWebpage(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
        

if __name__ == "__main__":
    application = tornado.web.Application(
    	handlers=[
            ("/ohlc", OHLCHandler),
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
