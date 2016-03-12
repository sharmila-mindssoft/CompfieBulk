#!/usr/bin/python

import argparse
from server.main import run_server

args_parser = argparse.ArgumentParser()
args_parser.add_argument(
    "port",
    help = "port to listen at (PORT)"
)

def parse_port(port) :
    try :
        port = int(port)
        assert (port > 0) and (port <= 65535)
        return port
    except Exception :
        return None

def main() :
    args = args_parser.parse_args()
    port = parse_port(args.port)
    if port is None :
        msg = "error: port is not in PORT format: %s"
        print msg % (args.port,)
        return
    run_server(port)

if __name__ == "__main__" :
    main()
