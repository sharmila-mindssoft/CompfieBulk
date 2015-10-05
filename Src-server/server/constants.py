import os

__all__ = [
	"ROOT_PATH",
    "HTTP_PORT",
]


#
# Constants
#

ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")

HTTP_PORT = 9080
