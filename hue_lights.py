#!/usr/bin/python
from qhue import Bridge
import matplotlib.pyplot as plt
import time

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

        self.lights_list = self.lights(refresh=True)

    def numLights(self):
        return len(self.lights)


    def lights_off(self):
        for light in self.lights():
            self.b.lights[light.num].state(on=False)

    def lights_on(self):
        for light in self.lights():
            self.b.lights[light.num].state(on=True)

    def colorloop(self, state):
        if state:
            eff = 'colorloop'
        else:
            eff = 'none'
        for light in self.lights_list:
            if light.on:
                self.b.lights[light.num].state(effect=eff)
                print "loop on"

    def lights(self, refresh = True):
        if refresh:
            raw_lights = self.b.lights
            t_lights = []
            for i in range(1, len(raw_lights()) + 1):
                raw_light = self.b.lights[i]()
                light = hue_light(raw_light,i)
                t_lights.append(light)
        else:
            t_lights = self.lights_list

        return t_lights

    def color_convert(self,colour):
        r = colour[0]
        g = colour[1]
        b = colour[2]

        if (r > 0.04045):
            red = pow((r + 0.055) / (1.0 + 0.055), 2.4)
        else:
            red = (r / 12.92)

        if (g > 0.04045):
            green = pow((g + 0.055) / (1.0 + 0.055), 2.4)
        else:
            green = (g / 12.92)
        if (b > 0.04045):
            blue = pow((b + 0.055) / (1.0 + 0.055), 2.4)
        else:
            blue = (b / 12.92)

        X = red * 0.664511 + green * 0.154324 + blue * 0.162028
        Y = red * 0.283881 + green * 0.668433 + blue * 0.047685
        Z = red * 0.000088 + green * 0.072310 + blue * 0.986039

        x = X / (X + Y + Z)
        y = Y / (X + Y + Z)

        return [x,y]

    def set_brightness(self,brightness=0,lights=None):
        if lights is None:
            lights = self.lights()

        for light in lights:
            self.b.lights[light.num].state(bri=brightness)

    def set_colour(self, colour=[0,0,0], lights=None):
        if lights is None:
            lights = self.lights()

        for light in lights:
            cc = self.color_convert(colour=colour)
            self.b.lights[light.num].state(xy=cc)

    def set_transition(self,tt):
        for light in self.lights():
            self.b.lights[light.num].state(transitiontime=tt)

    def set_saturation(self, sat):
        for light in self.lights():
            self.b.lights[light.num].state(sat=sat)

    def get_positions(self, lights = None):
        if lights is None:
            lights = self.lights()

        # ax.plot(np.random.rand(10))
        point ={}
        def onclick(event):
            print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  (event.button, event.x, event.y, event.xdata, event.ydata))

            plt.scatter(event.xdata, event.ydata, c='r', marker='o')
            point['key'] = [event.xdata, event.ydata]
            plt.draw()
            plt.close()

        points = []
        for light in lights:
            print "Enter position of " + light.name
            if points is not None:
                plt.scatter([item[0] for item in points], [item[1] for item in points])

            fig = plt.figure(1)
            plt.axis([0, 1, 0, 1])
            ax = fig.add_subplot(111)
            cid = fig.canvas.mpl_connect('button_press_event', onclick)
            plt.show()
            points.append(point['key'])

        return points




