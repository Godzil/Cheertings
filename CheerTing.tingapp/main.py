import tingbot
from tingbot import *
from colorsys import hsv_to_rgb
from colorsys import rgb_to_hsv
from copy import copy
import time
import requests

transition_time = 1 # seconds
transition_step = 100
current_colour = [0,0,0]
old_colour = [0,1,0]
colour_delta = [0,0,0]
colour_transition = False
transition_cur = 0
# setup code here

@every(seconds=5)
def get_last_color():
    global colour_transition, colour_delta, old_colour, current_colour, transition_cur, transition_step
    if colour_transition == False:
        r = requests.get('http://api.thingspeak.com/channels/1417/feed.json')
        j = r.json()
        f = j['feeds'][-8:]

        f = [element for index, element in enumerate(f) if index%2==0]
        col = f[0]
        # get the new colour
        channel = 1
        col = col['field2']
        r, g, b = tuple(ord(c) for c in col[1:].lower().decode('hex'))
        h,s,v = rgb_to_hsv(r,g,b)
        current_colour[0] = h
        current_colour[1] = s
        current_colour[2] = v
        #calculate the count for each
        for idx in range(0,3):
            colour_delta[idx] = (current_colour[idx] - old_colour[idx]) / float(transition_step)

        if old_colour != current_colour:
            colour_transition = True
            transition_cur = 0

@every(seconds=1.0/30)
def loop():
    global colour_transition, colour_delta, old_colour, current_colour, transition_cur, transition_step
    if colour_transition == True:
        # Do the transition
        for idx in range(0,3):
            old_colour[idx] += colour_delta[idx]
            r,g,b = hsv_to_rgb(old_colour[0],
                               old_colour[1],
                               old_colour[2]);
            screen.fill(color=(int(r),int(g), int(b)))
            screen.text("Cheertings", color=(255-int(r), 255-int(g), 255-int(b)))

        transition_cur += 1
        if transition_cur == transition_step:
            for idx in range(0,3):
                old_colour[idx] = current_colour[idx]
            colour_transition = False

tingbot.run()
