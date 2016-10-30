#!/usr/bin/python
from qhue import Bridge

# example light data
# {u'name': u'LivingColors 1',
# u'swversion': u'5.23.1.13452',
# u'manufacturername': u'Philips',
# u'state':
    #   {u'on': True,
    #   u'hue': 11668,
    #   u'colormode': u'hs',
    #   u'effect': u'none',
    #   u'alert': u'none',
    #   u'xy': [0.4457, 0.407],
    #   u'reachable': True,
    #   u'bri': 220,
    #   u'sat': 22},
    #   u'uniqueid': u'00:17:88:01:00:c2:c7:a8-0b',
    #   u'type': u'Color light',
    #   u'modelid': u'LLC011'}

class hue_light:
    # declare class variables

    def __init__(self, light_data, light_num):
        self.num = light_num
        self.index = light_num - 1
        self.name = light_data['name']
        self.swversion = light_data['swversion']
        self.manufacturername = light_data['manufacturername']
        self.uniqueid = light_data['uniqueid']
        self.type = light_data['type']
        self.modelid = light_data['modelid']

        state = light_data['state']
        self.on = state['on']
        self.hue = state['hue']
        self.colormode = str(state['colormode'])
        self.effect = str(state['effect'])
        self.alert = str(state['alert'])
        self.xy = state['xy']
        self.reachable = state['reachable']
        self.bri = state['bri']
        self.sat = state['sat']

        self.state = [self.on, self.hue, self.colormode,
                        self.effect, self.alert, self.xy,
                        self.reachable, self.bri, self.sat]


class bridge:

    def __init__(self, bridge_ip, username):
        self.b = Bridge(bridge_ip, username)
        num_lights = 0

        raw_lights = self.b.lights
        self.lights = []

        for i in range(1, len(raw_lights()) + 1):
            raw_light = self.b.lights[i]()
            light = hue_light(raw_light,i)
            self.lights.append(light)

    def numLights(self):
        return len(self.lights)

    def lights(self):
        return self.lights

    def lights_off(self):
        for light in self.lights:
            self.b.lights[light.num].state(on=False)

    def lights_on(self):
        for light in self.lights:
            self.b.lights[light.num].state(on=True)

    def colorloop(self, state):
        if state:
            eff = 'colorloop'
        else:
            eff = 'none'
        for light in self.lights:
            self.b.lights[light.num].state(effect=eff)


   # def set_light(self, ):
