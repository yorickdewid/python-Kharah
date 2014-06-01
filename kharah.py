import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import uuid
import os

data_dir = os.path.dirname(os.path.realpath(__file__))
static_path = os.path.join(data_dir, "static")

class WSHandler(tornado.websocket.WebSocketHandler):
    clients = []
    def open(self):
        print 'new connection'
        self.write_message("W00T")
        self.write_message("IDENTIFY")
        WSHandler.clients.append(17)
      
    def on_message(self, message):
        print 'message received %s' % message
        if message == 'COUNT':
            self.write_message("CLIENTS %d" % len(WSHandler.clients))
 
    def on_close(self):
      print 'connection closed'

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")

class ConsoleHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/hello', HelloHandler),
    (r'/console', ConsoleHandler),
    (r'/console/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application, ssl_options={
        "certfile": os.path.join(data_dir, "server.crt"),
        "keyfile": os.path.join(data_dir, "server.key")
    })
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
