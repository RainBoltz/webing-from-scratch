import tornado.ioloop
import tornado.web
import tornado.autoreload
import os, json
import random
import hashlib
import pandas as pd

class DBM:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = pd.read_csv(db_path, encoding='utf-8-sig')
    
    def check_exist(self, usr):
        for i in range(len(self.db)):
            if self.db.username.iloc[i] == usr:
                return i
        return -1
    
    def check_password(self, target_i, psw):
        h = hashlib.md5()
        h.update(psw.encode())
        psw_md5 = h.hexdigest()
        if self.db.password.iloc[target_i] == psw_md5:
            return True
        else:
            return False
            
    def new_user(self, usr, psw, eml):
        h = hashlib.md5()
        h.update(psw.encode())
        psw_md5 = h.hexdigest()
        
        uid = self.db.userid.iloc[len(self.db) - 1]
        
        self.db.loc[len(self.db)] = [uid, usr, psw_md5, eml]
        self.db.to_csv(self.db_path, index=False)

dbm = DBM("database.csv")

class loginHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            usr = self.get_argument("usr", None)
            psw = self.get_argument("psw", None)
            
            if not usr:
                self.write("please fill in username!")
            elif not psw:
                self.write("please fill in password!")
            else:
                target = dbm.check_exist(usr)
                if target == -1:
                    self.write("username not found!")
                elif not dbm.check_password(target, psw):
                    self.write("wrong password!")
                else:
                    self.write("login successfully!")
                    
        except:
            self.set_status(500)

class regHandler(tornado.web.RequestHandler):
    def post(self):
        #try:
        usr = self.get_argument("usr", None)
        psw = self.get_argument("psw", None)
        eml = self.get_argument("eml", None)
        
        if not usr:
            self.write("please fill in username!")
        elif not psw:
            self.write("please fill in password!")
        else:
            target = dbm.check_exist(usr)
            if target != -1:
                self.write("username has already existed!")
            else:
                dbm.new_user(usr, psw, eml)
                self.write("registration completed!")
                    
        #except:
        #    self.set_status(500)            
            
class MainWebpage(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
        
class loginWebpage(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')
        
class regWebpage(tornado.web.RequestHandler):
    def get(self):
        self.render('register.html')


if __name__ == "__main__":

    application = tornado.web.Application(
    	handlers=[
            ("/valid/login", loginHandler),
            ("/valid/register", regHandler),
            (r"/register", regWebpage),
            (r"/login", loginWebpage),
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