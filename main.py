#!/usr/bin/env python3


# from pybricks.hubs import EV3Brick
# from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
#                                  InfraredSensor, UltrasonicSensor, GyroSensor)
# from pybricks.parameters import Port, Stop, Direction, Button, Color
# from pybricks.tools import wait, StopWatch, DataLog
# from pybricks.robotics import DriveBase
# from pybricks.media.ev3dev import SoundFile, ImageFile
from ev3dev2.sensor import Sensor, INPUT_1
from ev3dev2.port import LegoPort
from ev3dev2.sound import Sound
from threading import Thread
# from pybricks.messaging import BluetoothMailboxServer, TextMailbox
import os
import sys
import time
import socket

from odometrium.main import Odometrium
from smbus import SMBus
# from main_master import Master_Bot



#Faire une classe Slave Robot en prenant toutes les fonction du dessous
class Slave_Bot():
    def __init__(self):

        self.position = Odometrium(left='A', right='D', wheel_diameter=5.5, wheel_distance=12,
                      count_per_rot_left=None, count_per_rot_right=360, debug=False,
                      curve_adjustment=1)

        self.x = self.position.x
        self.y = self.position.y
        # self.serverMACAddress = '172.24.12.207'
        # self.port = 1050
        # self.s = socket.socket()
        # print("A")
        # self.s.connect((self.serverMACAddress,self.port))
        # print("B")
        self.orientation = self.position.orientation

        self.loop = True

    # def server_connection(self):

    #     server = BluetoothMailboxServer()
        
    #     server.wait_for_connection()

    def forward(self):
        if self.loop == True:
            self.position.move(left=-100, right=-100, time=6)
    def forward_low(self):
        if self.loop == True:
            self.position.move(left=-100, right=-100, time=5)        
 
    def turn_right_180(self):
        if self.loop == True:
            self.position.move(left=-100, right=0, time=4)

    def turn_left_180(self):
        if self.loop == True:
            self.position.move(left=0, right=-100, time=4)

    def moving_pattern(self):        
        
        #c'est ici qu'on va créer le pattern à l'aide de la fonction move de odemetrium en gardant la position connu
        while self.loop:

            # self.position.move(left=-100, right=-100, time=5)
            self.forward()
            self.turn_right_180()
            self.forward()
            self.turn_right_180()
            self.forward()
            self.turn_left_180()
            # self.position.move(left=-100, right=0, time=4)
            # self.position.move(left=-100, right=-100, time=5)
            # self.position.move(left=-100, right=0, time=4)
            # self.position.move(left=-100, right=-100, time=5)
            # self.position.move(left=0, right=-100, time=4)

            pos = self.get_position()
            # print(pos)

        #on prend les information x, y et l'orientation qu'on va renvoyer en sortie de la fonction
        
    
    def get_position(self):

        return self.x,self.y,self.orientation


    def distance_calculation(self,w,h):
        #Regression linéaire avec les données dans le data.csv
        distance_estim = 58.5446 + 0.5136*w - 1.2978*h
        # size_px_init = 60
        # distance_init = 20
        print("#",int(w))
        spkr = Sound()
        spkr.speak('Distance calculated !')
        spkr.speak(str(distance_estim))
        # return (size_px_init*distance_init)/w
        return distance_estim




    def pixy_camera(self):

        in1 = LegoPort(INPUT_1)
        in1.mode = 'other-i2c'
        # Short wait for the port to get ready
        time.sleep(0.5)

        bus = SMBus(3)
        address = 0x54
        sigs = 2

        # Data for requesting block
        data = [174, 193, 32, 2, sigs, 1]

        # Read and display data until TouchSensor is pressed
        while True:

            # Request block
            bus.write_i2c_block_data(address, 0, data)
            # Read block
            block = bus.read_i2c_block_data(address, 0, 20)

            if block[6]==2:

                # Extract data
                sig = block[7]*256 + block[6]
                x = block[9]*256 + block[8]
                y = block[11]*256 + block[10]
                w = block[13]*256 + block[12]
                h = block[15]*256 + block[14]
                spkr = Sound()
                self.loop = False
                self.position.stop()
                pos = self.get_position()
                spkr.speak('Target detected !')
                dis = self.distance_calculation(w,h)
                print("distance :", dis)
                # self.s.send(int(dis))
                
                #insert here call of function distance with x,y,w,h and pos inputs 





def set_font(name):
    '''Sets the console font

    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)


def main():
    '''The main function of our program'''

    set_font('Lat15-Terminus24x12')
    # moteur
    bot = Slave_Bot()
    t = Thread(target=bot.moving_pattern)
    t.start()
    
    bot.pixy_camera()
    # bot = Master_Bot()
    # bot.server_connection()
    # bot.receive_distance()


    """
    ev3.speaker.beep(frequency=1000, duration=500)
    ev3.speaker.beep(frequency=800, duration=200)
    ev3.speaker.beep(frequency=1000, duration=500)
    ev3.speaker.beep(frequency=800, duration=200)
    """

    #ev3.speaker.beep()

if __name__ == "__main__" :
    main()