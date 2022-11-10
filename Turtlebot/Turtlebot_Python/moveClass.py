#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
from time import sleep
import sys, select, tty, termios

class bot:
    def __init__(self) -> None:
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.connect("localhost")
        self.client.loop_start()
        self.settings = termios.tcgetattr(sys.stdin)
        self.lin_vel = 0.0
        self.ang_vel = 0.0
        pass
    def on_connect(self, client, userdata, flags, rc):
        print('Connected with result code: {}'.format(rc))
    
    def on_disconnect(self, client, userdata, rc):
        print('Disconnected with result code: {}'.format(rc))
        if rc != 0:
            print('Unexpected disconnection, might be a network error...')
    
    def on_message(self, client, userdata, msg):
        message = msg.payload.decode("utf-8")
        print('Recieved message. Topic: {}, message: {}'.format(msg.topic, message))
        if msg.topic == 'test_sub_topic':
            # do stuff
            print('Check.')
        else:
            print('Not a topic to react on.')
    
    def move(self, lin = 0, ang = 0, time = 0):
        pub_msg = { 'linear' : {'x':lin, 'y':0, 'z':0},
                        'angular' : {'x':0, 'y':0, 'z':ang}}
        pub_msg = json.dumps(pub_msg)
        self.client.publish('cmd_vel', payload=pub_msg)
        sleep(time)
    
    def __del__(self):
        pub_msg = { 'linear' : {'x':0, 'y':0, 'z':0},
                        'angular' : {'x':0, 'y':0, 'z':0}}
        pub_msg = json.dumps(pub_msg)
        info = self.client.publish('cmd_vel', payload=pub_msg)
        info.wait_for_publish()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)