#!/usr/bin/python

from qhue import Bridge
import time
import hue_lights


username = 'XFRBw2bgZuE6ERAhkBx4OCNvSYDBAGGwZOvfr9D8'
bridge_ip = "192.168.0.2"

bridge = hue_lights.bridge(bridge_ip,username)

for light in bridge.lights:
    print light.name, light.state



#b.lights[1].state(bri=200, hue=9000)
