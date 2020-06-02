#!/usr/bin/env python

from sense_emu import SenseHat
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource


# Define RGB colors
red = (255,0,0)
green = (0,255,0)
white = (255,255,255)


class TempResource(Resource):
    def __init__(self, name="TempResource", coap_server=None):
        super(TempResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)

        self.payload = "Temperature Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET(self, request):
        # Instantiate SenseHat sensor
        sense = SenseHat()
        self.payload = str(sense.get_temperature())
        return self

class HumidityResource(Resource):
    def __init__(self, name="HumidityResource", coap_server=None):
        super(HumidityResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)

        self.payload = "Humidity Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET(self, request):
        # Instantiate SenseHat sensor
        sense = SenseHat()
        self.payload = str(sense.get_humidity())
        return self

class LEDResource(Resource):
    def __init__(self, name="LEDResource", coap_server=None):
        super(LEDResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)

        self.payload = "LED Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_POST(self, request):
        # Instantiate SenseHat sensor
        sense = SenseHat()
        sense.clear(red)
        self.payload = "OK"
        return self
