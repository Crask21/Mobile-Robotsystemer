import paho.mqtt.client as mqtt
import json
from time import sleep
import sys, select, tty, termios

msg = """
Current code tests a movement class
---------------------------
"""
e = """
Communications Failed
"""
class movement:
    def __init__(self, movementList) -> None:
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        #self.client.connect("192.168.0.6")
        self.client.connect("localhost")
        # Start a non-blocking loop
        self.client.loop_start()
        # or if not needed, a blocking loop can be called
        # Used for handling input from the terminal..
        self.settings = termios.tcgetattr(sys.stdin)

        self.lin_vel = 0.0
        self.ang_vel = 1.0
        
    def on_connect(self, client, userdata, flags, rc):
        print('Connected with result code: {}'.format(rc))
        # Subscribe to topics
        #client.subscribe([("topic1", QoS), ("topic2", QoS), ...])
        #client.subscribe('test_sub_topic',1)

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

    def run(self):
        # Do stuff that will not return until the mqtt connection is not needed anymore..
        # ie. send a command every 20 ms and read input to increase/decrease velocities
        # It is wrapped in a try, except, finally statement such that CTRL-C will stop the robot..
        try:
            print(msg)
            while True:
                key = self.get_key()
                if key == 'w':
                    self.lin_vel += 0.02
                    #print('Current velocities. Linear: {:.2f}, angular: {:.2f}'.format(self.lin_vel self.ang_vel),end='\r', flush=True)
                elif key == 'a':
                    self.ang_vel += 0.1
                    #print('Current velocities. Linear: {:.2f}, angular: {:.2f}'.format(self.lin_vel, self.ang_vel),end='\r', flush=True)
                elif key == 'x':
                    self.lin_vel -= 0.02
                    #print('Current velocities. Linear: {:.2f}, angular: {:.2f}'.format(self.lin_vel, self.ang_vel),end='\r', flush=True)
                elif key == 'd':
                    self.ang_vel -= 0.1
                    #print('Current velocities. Linear: {:.2f}, angular: {:.2f}'.format(self.lin_vel, self.ang_vel),end='\r', flush=True)
                elif key == 's' or key == ' ':
                    self.lin_vel = 0.0
                    self.ang_vel = 0.0
                    #print('Current velocities. Linear: {:.2f}, angular: {:.2f}'.format(self.lin_vel, self.ang_vel),end='\r', flush=True)
                else:
                    if key == '\x03':
                        # ESC key
                        break

                # This is where the magic happens
                pub_msg = { 'linear' : {'x':self.lin_vel, 'y':0, 'z':0},
                        'angular' : {'x':0, 'y':0, 'z':self.ang_vel}}
                #pub_msg['linear']['x'] = 0.8
                pub_msg = json.dumps(pub_msg)
                # And publish the message through MQTT
                self.client.publish('cmd_vel', payload=pub_msg)
                # The motor speeds timeout is 500ms, so an update frequency > 2 Hz should be enough
                # Set higher here since it is easier to read keyboard input with high frequency..
                sleep(0.02)
        except:
            print(e)
        finally:
            # Stop the robot when CTRL-C is pressed
            pub_msg = { 'linear' : {'x':0, 'y':0, 'z':0},
                        'angular' : {'x':0, 'y':0, 'z':0}}
            pub_msg = json.dumps(pub_msg)
            info = self.client.publish('cmd_vel', payload=pub_msg)
            info.wait_for_publish()
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)

    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key
    
def main():
    moveObj = movement()
    

if __name__ == "__main__":
    main()