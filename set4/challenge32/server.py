import tornado.web
import time
from set4_28 import * 
DELAY = 0.001
key = b'YELLOW SUBMARINE'

"""
with help from
https://github.com/wangray/matasano-crypto/blob/master/set4/timing_server.py

"""
def insecure_compare(filename,signature):
    signature = signature.encode('ascii')
    filename = filename.encode('ascii')
    actual_signature = SHA_1(key+filename).encode('ascii')
    for i in range(len(signature)):
        if signature[i] != actual_signature[i]:
            return False 
        time.sleep(DELAY)
    return True 
    




class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Nothing to show, move along...')

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        filename = self.get_argument("file", None, True)
        signature = self.get_argument("signature", None, True)

        self.write("filename: " + filename + "<br>")
        self.write("signature " + signature + "<br>")

        if not insecure_compare(filename, signature):
            self.set_status(500)
            self.finish("<html><body>HMAC Check failed</body></html>")
        else:
            self.write("HMAC Check OK")


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/test", TestHandler)
    ])

    application.listen(8080)
    tornado.ioloop.IOLoop.current().start()
