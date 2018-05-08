from tornado.ioloop import IOLoop as TornadoIOLoop

__all__ = [
    "IOLoop"
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
