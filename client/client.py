#!/usr/bin/env python2
import getopt
import socket
import sys
import time

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri

client = None


def usage():
    print("Command:\tclient.py -o -p [-P]")
    print("Options:")
    print("\t-o, --operation=\tGET|PUT|POST|DELETE|DISCOVER|OBSERVE")
    print("\t-p, --path=\t\t\tPath of the request")
    print("\t-P, --payload=\t\tPayload of the request")
    print("\t-f, --payload-file=\t\tFile with payload of the request")


def client_callback(response):
    print("Callback")


def client_observer(path):
    global client
    temp_t = client.get("/temp_threshold").payload
    humi_t = client.get("/humi_threshold").payload
    print("Starting in observer mode...")
    print("Updating information every 2 seconds...\n")
    time.sleep(2)
    while True:
        if temp_t != client.get("/temp_threshold").payload:
            temp_t = client.get("/temp_threshold").payload
            print("NEW TEMPERATURE THRESHOLD DETECTED!")
            print("Temperature = " + client.get("/temp").payload + "\t\tTemperature Threshold = " + client.get("/temp_threshold").payload)
        else:
            print("Temperature = " + client.get("/temp").payload + "\t\tTemperature Threshold = " + client.get("/temp_threshold").payload)
        if humi_t != client.get("/humi_threshold").payload:
            humi_t = client.get("/humi_threshold").payload
            print("NEW HUMIDITY THRESHOLD DETECTED!")
            print("Humidity = " + client.get("/humi").payload + "\t\tHumidity Threshold = " + client.get("/humi_threshold").payload)
        else:
            print("Humidity = " + client.get("/humi").payload + "\t\tHumidity Threshold = " + client.get("/humi_threshold").payload)
        time.sleep(2)


def main():
    global client
    op = None
    path = None
    payload = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:p:P:f:", ["help", "operation=", "path=", "payload=",
                                                               "payload_file="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-o", "--operation"):
            op = a
        elif o in ("-p", "--path"):
            path = a
        elif o in ("-P", "--payload"):
            payload = a
        elif o in ("-f", "--payload-file"):
            with open(a, 'r') as f:
                payload = f.read()
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            usage()
            sys.exit(2)

    if op is None:
        print("Operation must be specified")
        usage()
        sys.exit(2)

    if path is None:
        print("Path must be specified")
        usage()
        sys.exit(2)

    if not path.startswith("coap://"):
        print("Path must be conform to coap://host[:port]/path")
        usage()
        sys.exit(2)

    host, port, path = parse_uri(path)
    try:
        tmp = socket.gethostbyname(host)
        host = tmp
    except socket.gaierror:
        pass
    client = HelperClient(server=(host, port))
    if op == "GET":
        if path is None:
            print("Path cannot be empty for a GET request")
            usage()
            sys.exit(2)
        response = client.get(path)
        print(response.pretty_print())
        client.stop()
    elif op == "OBSERVE":
        if path is None:
            print("Path cannot be empty for a GET request")
            usage()
            sys.exit(2)
        client_observer(path)
    elif op == "POST":
        if path is None:
            print("Path cannot be empty for a POST request")
            usage()
            sys.exit(2)
        if payload is None:
            print("Payload cannot be empty for a POST request")
            usage()
            sys.exit(2)
        response = client.post(path, payload)
        print(response.pretty_print())
        client.stop()
    else:
        print("Operation not recognized")
        usage()
        sys.exit(2)


if __name__ == '__main__':
    main()
