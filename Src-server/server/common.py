import types
import tornado.netutil
import tornado.httpserver
import tornado.web

from tornado.ioloop import IOLoop as TornadoIOLoop

__all__ = [
    "IOLoop",
    "WebServer",
    "WebRequest",
    "WebResponse",
    "cors_handler"
]



class IOLoop(object) :
    NONE = TornadoIOLoop.NONE
    READ = TornadoIOLoop.READ
    WRITE = TornadoIOLoop.WRITE
    ERROR = TornadoIOLoop.ERROR

    def __init__(self) :
        self._tornado_io_loop = TornadoIOLoop()

    def inner(self) :
        return self._tornado_io_loop

    def close(self, all_fds=False) :
        self._tornado_io_loop.close(all_fds)

    def add_handler(self, fd, handler, events) :
        self._tornado_io_loop.add_handler(fd, handler, events)

    def update_handler(self, fd, events) :
        self._tornado_io_loop.update_handler(fd, events)

    def remove_handler(self, fd) :
        self._tornado_io_loop.remove_handler(fd)

    def start(self) :
        self._tornado_io_loop.start()

    def stop(self) :
        self._tornado_io_loop.stop()

    def time(self) :
        return self._tornado_io_loop.time()

    def add_timeout(self, deadline, callback) :
        return self._tornado_io_loop.add_timeout(deadline, callback)

    def remove_timeout(self, timeout) :
        self._tornado_io_loop.remove_timeout(timeout)

    def add_callback(self, callback, *args, **kwargs) :
        self._tornado_io_loop.add_callback(callback, *args, **kwargs)

    def run(self) :
        try :
            self.start()
        except KeyboardInterrupt :
            print ""
            print "Ctrl-C recieved. Exiting."

#
# RequestHandler
#
METHODS = set([
    "GET", "HEAD", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"
])

class RequestHandler(tornado.web.RequestHandler) :
    __default_headers = {}
    def initialize(self, handler_map) :
        self.__handler_map = handler_map
        self.__close_callback = None
        for method, handler in self.__handler_map.items() :
            assert method in METHODS
            obj_method = self.__make_object_method(handler)
            setattr(self, method.lower(), obj_method)

    def set_default_headers(self) :
        for name, value in self.__default_headers.items() :
            self.set_header(name, value)

    def internal_add_default_header(self, name, value) :
        self.__default_headers[name] = value

    def __make_object_method(self, handler) :
        @tornado.web.asynchronous
        def object_method(self, *arguments) :
            request = WebRequest(self, arguments)
            response = WebResponse(self)
            handler(request, response)
        return types.MethodType(object_method, self)

    def set_close_callback(self, close_callback) :
        self.__close_callback = close_callback

    def on_connection_close(self) :
        if self.__close_callback is not None :
            self.__close_callback()


#
# WebRequest
#

class UploadedFile(object) :
    def __init__(self, file_name, content_type, body) :
        self._file_name = file_name
        self._content_type = content_type
        self._body = body

    def file_name(self) : return self._file_name
    def content_type(self) : return self._content_type
    def body(self) : return self._body

    def __repr__(self) :
        return "UploadedFile(%s, %s, size=%s)" % (
            repr(self._file_name), repr(self._content_type), len(self._body)
        )

class WebRequest(object) :
    def __init__(self, inner, arguments) :
        self._inner = inner
        self._arguments = arguments

    def arguments(self) :
        return self._arguments

    def parameter(self, name, strip=True) :
        return self._inner.get_argument(name, default=None, strip=strip)

    def parameters(self, name, strip=True) :
        return self._inner.get_arguments(name, strip=strip)

    def query_parameter(self, name, strip=True) :
        return self._inner.get_guery_argument(name, default=None, strip=strip)

    def query_parametes(self, name, strip=True) :
        return self._inner.get_guery_arguments(name, strip=strip)

    def body_parameter(self, name, strip=True) :
        return self._inner.get_body_argument(name, default=None, strip=strip)

    def body_parameters(self, name, strip=True) :
        return self._inner.get_body_arguments(name, strip=strip)

    def protocol(self) :
        return self._inner.request.protocol

    def method(self) :
        return self._inner.request.method

    def uri(self) :
        return self._inner.request.uri

    def path(self) :
        return self._inner.request.path

    def query(self) :
        return self._inner.request.query

    def content_type(self) :
        return self.header("Content-Type")

    def header(self, name) :
        return self._inner.request.headers.get(name)

    def get_cookie(self, name):
        self._inner.request.cookies.get(name)

    def all_headers(self) :
        return self._inner.request.headers.get_all()

    def remote_ip(self) :
        return self._inner.request.remote_ip

    def host(self) :
        return self._inner.request.host

    def body(self) :
        return self._inner.request.body

    def files(self) :
        def convert_file(e) :
            return UploadFile(e["filername"], e["content_type"], e["body"])
        result = {}

        for key, entries in self._inner.request.files.items() :
            entries1 = [convert_file(e) for e in entries]
            result[key] = entries1
        return result

    def set_close_callback(self, close_callback) :
        self._inner_set_close_callback(close_callback)


#
# WebResponse
#

class WebResponse(object) :
    def __init__(self, response) :
        self._response = response

    def set_default_header(self, name, value) :
        self._response.internal_add_default_header(name, value)
        self._response.set_header(name, value)

    def set_status(self, status_code, reason=None) :
        self._response.set_status(status_code, reason)

    def set_content_type(self, value) :
        self.set_header("Content-Type", value)

    def set_header(self, name, value) :
        self._response.set_header(name, value)

    def set_cookie(self, name, value) :
        self._response.set_cookie(name, value)

    def add_header(self, name, value) :
        self._response.add_header(name, value)

    def send(self, body=None) :
        if body is not None :
            self._response.write(body)
        self._response.finish()

    def redirect(self, url, permanent=False, status=None) :
        self._response.redirect(url, permanent=permanent, status=status) 


#
# WebServer
#

class WebServer(object) :
    def __init__(self, io_loop) :
        self._io_loop = io_loop
        self._application_urls = []
        self._application = None
        self._http_server = None

    def low_level_url(self, url, handler_class, *args) :
        assert self._application is None
        entry = (url, handler_class) + args
        self._application_urls.append(entry)

    def url(self, url, **handler_map) :
        assert self._application is None
        options = dict(handler_map=handler_map)
        self.low_level_url(url, RequestHandler, options)

    def start(self, port_or_address, lower_level_handlers=None, backlog=128) :
        assert self._application is None

        if lower_level_handlers is not None :
            for entry in lower_level_handlers :
                self.low_level_url(*entry)

        self._application = tornado.web.Application(
            self._application_urls,
            gzip=True
        )
        self._http_server = tornado.httpserver.HTTPServer(
            self._application,
            io_loop = self._io_loop.inner(),
            xheaders = True
        )

        if type(port_or_address) in (tuple, list) :
            ip_address, port = port_or_address
        else :
            ip_address = ""
            port = port_or_address

        sockets = tornado.netutil.bind_sockets(
            port, address=ip_address, backlog=backlog
        )

        self._http_server.add_sockets(sockets)

#
# cors_handler
#

def cors_handler(request, response):
    if True :
        print ""
        print "CORS OPTIONS REQUEST"
        print "METHOD: %s" % (request.method(),)
        print "URL: %s" % (request.path(),)
        print "REQUEST:",
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Headers", "Content-Type")
    response.set_header("Access-Control-Allow-Methods", "POST")
    response.set_status(204)
    response.send("")
