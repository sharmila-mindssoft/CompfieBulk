#!/usr/bin/python

import argparse
import socket
from server.clientmain import run_server

args_parser = argparse.ArgumentParser()
args_parser.add_argument(
    "address",
    help="Address to listen at ((IP:PORT)"
)
args_parser.add_argument(
    "knowledge_server_ip_address",
    help="Knowledge server ip address (IP:PORT)"
)


def parse_port(port):
    try:
        port = int(port)
        assert (port > 0) and (port <= 65535)
        return port
    except Exception:
        return None

def parse_ip_address(ip_address):
    ip = None
    port = None
    try:
        ip_address = ip_address.split(":")
        ip = ip_address[0].strip()
        socket.inet_aton(ip)
        port = ip_address[1].strip()
        port = parse_port(port)
        if port is None:
            return None
    except Exception:
        return None
    assert ip is not None
    assert port is not None
    return (ip, port)


def main() :
    args = args_parser.parse_args()
    address = parse_ip_address(args.address)
    if address is None:
        msg = "error: ip address is not in IP:PORT format: %s"
        print msg % (args.address,)
        return
    knowledge_server_ip_address = parse_ip_address(
        args.knowledge_server_ip_address
    )
    if knowledge_server_ip_address is None:
        msg = "error: knowledge server ip address is not in IP:PORT format: %s"
        print msg % (args.knowledge_server_ip_address,)
        return
    run_server(address, knowledge_server_ip_address)

if __name__ == "__main__" :
    main()
