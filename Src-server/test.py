from tornado.httpclient import AsyncHTTPClient
from basics.ioloop import IOLoop

io_loop = IOLoop()

def handle_request(response):
    if response.error:
        print "Error:", response.error
    else:
        print response.body

def delay_initialize():
    http_client = AsyncHTTPClient()
    http_client.fetch("http://www.google.com/", handle_request)

io_loop.add_callback(delay_initialize)
io_loop.run()
