#!/usr/bin/env python2

import getopt
import sys
import threading
import time

from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from sense_emu import SenseHat

from resources import TempResource
from resources import HumidityResource
from resources import LEDResource

red = (255,0,0)
black = (0,0,0)
temp_t = 24.0
humi_t = 60.0


def actuator_observer():
    sense = SenseHat()
    global temp_t
    global humi_t
    while True:
        time.sleep(1)
        print("TT = " + str(temp_t) + "\tTemp = " + str(sense.get_temperature()) + "\tHU= " + str(humi_t) + "\tHumidity = " + str(sense.get_humidity()))
        if sense.get_temperature() > float(temp_t) or sense.get_humidity() > float(humi_t):
            sense.clear(red)
        else:
            sense.clear(black)


class TempThreshold(Resource):
    def __init__(self, name="TempThreshold", coap_server=None):
        super(TempThreshold, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)

        self.payload = "Temperature Threshold Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET(self, request):
        global temp_t
        self.payload = str(temp_t)
        return self

    def render_POST(self, request):
        global temp_t
        temp_t = request.payload
        self.payload = "OK"
        return self


class HumiThreshold(Resource):
    def __init__(self, name="HumiThreshold", coap_server=None):
        super(HumiThreshold, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)

        self.payload = "Humidity Threshold Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET(self, request):
        global humi_t
        self.payload = str(humi_t)
        return self

    def render_POST(self, request):
        global humi_t
        humi_t = request.payload
        self.payload = "OK"
        return self


class CoAPServer(CoAP):
    def __init__(self, host, port, multicast=False):
        CoAP.__init__(self, (host, port), multicast)
        self.add_resource('/temp', TempResource())
        self.add_resource('/temp_threshold', TempThreshold())
        self.add_resource('/humi', HumidityResource())
        self.add_resource('/humi_threshold', HumiThreshold())
        # self.add_resource('/led', LEDResource())

        print("CoAP Server started on " + host + ":" + str(port))
        print(self.root.dump())


def usage():
    print("controller.py -i <ip address> -p <port> -s coap://<ip address>:<server port>/<path>")


def main(argv):
    ip = "0.0.0.0"
    port = 5683
    multicast = False
    server = None
    name = "MyName"
    path = None
    try:
        opts, args = getopt.getopt(argv, "hi:p:m:n:s", ["ip=", "port=", "multicast", "name=", "server="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--ip"):
            ip = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-m", "--multicast"):
            multicast = True
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-s", "--server"):
            server = arg

    if server is None:
        print("Working in standalone mode... indicate the server address to connect to a server")
        usage()
    else:
        host, port, path = parse_uri(server)
        print("server = " + server)
        print("host = " + host)
        print("port = " + str(port))
        print("path = " + path)

        payload = "coap://" + ip + ":" + str(port)
        client = HelperClient(server=(host, port))
        response = client.post(path, payload)
        print(response)

    server = CoAPServer(ip, port, multicast)
    try:
        t1 = threading.Thread(target=actuator_observer)
        t1.start()
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")


if __name__ == "__main__":
    main(sys.argv[1:])
