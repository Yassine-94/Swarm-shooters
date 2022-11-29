#!/usr/bin/env python3

from ev3dev2.sensor import Sensor, INPUT_1, INPUT_2
from ev3dev2.port import LegoPort
from ev3dev2.sound import Sound
from threading import Thread
import os
import sys
import time
import socket
from odometrium.main import Odometrium
from smbus import SMBus
import ev3dev.ev3 as ev3
# from main_master import Master_Bot


#Faire une classe Slave Robot en prenant toutes les fonction du dessous
class Slave_Bot():
    def __init__(self):
        self.position = Odometrium(left='A', right='D', wheel_diameter=5.5, wheel_distance=12,
                      count_per_rot_left=None, count_per_rot_right=360, debug=False,
                      curve_adjustment=1)
        self.x = self.position.x
        self.y = self.position.y

        self.serverAddress = '169.254.2.221'
        self.port = 1050
        self.size = 1024
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.serverAddress,self.port))
        self.orientation = self.position.orientation
        self.shooting_part = ev3.LargeMotor('outC')
        self.loop = True
        

    # def server_connection(self):
    #     server = BluetoothMailboxServer()
    #     server.wait_for_connection()

    # fonction pour avancer
    def forward(self):
        if self.loop == True:
            self.position.move(left=-150, right=-150, time=14)
    # fonction pour avancer moins vite
    def forward_low(self):
        if self.loop == True:
            self.position.move(left=-100, right=-100, time=5)  
    # fonction pour tourner à droite      
    def turn_right_180(self):
        if self.loop == True:
            self.position.move(left=-95, right=0, time=5)
    # fonction pour tourner à gauche
    def turn_left_180(self):
        if self.loop == True:
            self.position.move(left=0, right=-100, time=4)

    def moving_pattern(self):
        #c'est ici qu'on va créer le pattern à l'aide de la fonction move de odemetrium en gardant la position connu
        while self.loop:
            
            self.forward()
            self.turn_right_180()
            self.forward()
            self.turn_right_180()
            self.forward()
            self.turn_right_180()
            self.forward()
            self.turn_right_180()
 
            # pos = self.get_position()
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
        spkr.speak(int(distance_estim))
        # return (size_px_init*distance_init)/w
        return distance_estim

    def pixy_camera(self):
        in1 = LegoPort(INPUT_1)
        in1.mode = 'other-i2c'
        # Short wait for the port to get ready
        time.sleep(0.5)
        bus = SMBus(3)
        address = 0x54
        sigs = 1
        # Data for requesting block
        data = [174, 193, 32, 2, sigs, 1]
        # Read and display data until TouchSensor is pressed
        while True:
           
            # Request block
            bus.write_i2c_block_data(address, 0, data)
            # # Read block
            block = bus.read_i2c_block_data(address, 0, 20)
            print("block 6 = ",block[6], "block 7 = ", block[7])
            time.sleep(3)
            # distance= '11'
            # data = distance.encode("utf8")
            # self.s.send(data)
            # self.shooting()
            # break
            if block[6]==1:
                print("dedans")
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
                print("largeur :", w)
                print("hauteur :", h)
                dis = int(dis)
                dis = str(dis)
                data = dis.encode("utf8")
                self.s.send(data)
                self.shooting()
                break
                
                #insert here call of function distance with x,y,w,h and pos inputs 

    # communication, envoyer les données au master
    # def send_data(self):
    #     data = self.distance_calculation()
    #     data = data.encode("utf8")
    #     socket.sendall(data)
    '''
    def send_data(self):
        spk = Sound()
        spk.speak('Connection')
        data = spk.encode("utf8")
        socket.sendall(data)'''

    def shooting(self):
        # time.sleep(5000)
        while 1:
            data_shooting1 = self.s.recv(self.size)
            data_shooting = data_shooting1.decode('utf8')
            print("detected")
            if data_shooting is not None:
                spk = Sound()
                spk.speak('I received it !')        
                self.shooting_part.run_timed(time_sp=5 * 1000, speed_sp=200)
                time.sleep(2)
                self.shooting_part.run_timed(time_sp=3 * 1000, speed_sp=-200)
                time.sleep(2)
                self.shooting_part.run_timed(time_sp=5 * 1000, speed_sp=200)
                time.sleep(2)
                self.shooting_part.run_timed(time_sp=3 * 1000, speed_sp=-200)
                
                break
        





def set_font(name):
    '''Sets the console font
    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)

def main():
    '''The main function of our program'''
    set_font('Lat15-Terminus24x12')

    bot = Slave_Bot()
    t = Thread(target=bot.moving_pattern)
    t.start()
    bot.pixy_camera()


    # bot = Master_Bot()
    # bot.server_connection()
    # bot.receive_distance()

if __name__ == "__main__" :
    main()
