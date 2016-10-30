#!/usr/bin/python
import hue_lights
import time

username = 'XFRBw2bgZuE6ERAhkBx4OCNvSYDBAGGwZOvfr9D8'
bridge_ip = "192.168.0.2"

bridge = hue_lights.bridge(bridge_ip,username)

for light in bridge.lights:
    print light.name, light.state

#bridge.colorloop(True)
bridge.colorloop(False)

bridge.lights_off()

# for i in range(0,100):
#     bridge.lights_off()
#     time.sleep(0.1)
#     bridge.lights_on()

