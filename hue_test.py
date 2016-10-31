#!/usr/bin/python
import hue_lights
import time
import random


username = 'XFRBw2bgZuE6ERAhkBx4OCNvSYDBAGGwZOvfr9D8'
bridge_ip = "192.168.0.2"

bridge = hue_lights.bridge(bridge_ip,username)

for light in bridge.lights(refresh = False):#lights:
    print light.name, light.state

bridge.lights_on()
lights = bridge.lights()
bridge.set_brightness(brightness=100)

print bridge.get_positions()

#bridge.lights_off()

#bridge.set_colour([10,30,100])
