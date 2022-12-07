#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
from time import sleep
import sys, select, tty, termios

class moveClass:
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
    
    def drive(self, lin = 0.0, ang = 0.0, time = 0.02):
        pub_msg = { 'linear' : {'x':lin, 'y':0, 'z':0},
                        'angular' : {'x':0, 'y':0, 'z':ang}}
        pub_msg = json.dumps(pub_msg)
        self.client.publish('cmd_vel', payload=pub_msg)
        sleep(time)
    
    def move(self,ang = 0.0, dist = 0.0):
        #posibly need to take into account negative movement
        dist = float(dist)
        ang = float(ang)
        if(ang !=0):
            for i in range(int(abs(ang)/45)):
                self.drive(0,ang/abs(ang)*1.6,0.5)
            self.drive(0,(abs(ang)%45)/45*1.6*abs/abs(ang),0.5)
        else:
            print("An angle was 0")
    
        if(dist != 0):
            for i in range(int(abs(dist)/10)):
                self.drive(dist/abs(dist)*0.2,0,0.5)
            self.drive((dist%10)*0.02*dist/abs(dist))
        else:
            print("A distance was 0")

    def stop(self, delay = 0.02):
        self.drive(0,0,delay)

    def __del__(self):
        pub_msg = { 'linear' : {'x':0, 'y':0, 'z':0},
                        'angular' : {'x':0, 'y':0, 'z':0}}
        pub_msg = json.dumps(pub_msg)
        info = self.client.publish('cmd_vel', payload=pub_msg)
        info.wait_for_publish()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)