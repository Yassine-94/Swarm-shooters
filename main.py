#!/usr/bin/env python3

from ev3dev2.sensor import Sensor, INPUT_1, INPUT_2
from ev3dev2.port import LegoPort
from ev3dev2.sound import Sound
from sys import stderr
from threading import Thread
import os
import sys
import time
import socket
from odometrium.main import Odometrium
from smbus import SMBus
import ev3dev.ev3 as ev3



#Faire une classe Slave Robot en prenant toutes les fonction du dessous
class Slave_Bot():
    def __init__(self):
        self.position = Odometrium(left='A', right='D', wheel_diameter=5.5, wheel_distance=12,
                      count_per_rot_left=None, count_per_rot_right=360, debug=False,
                      curve_adjustment=1)
        self.x = self.position.x
        self.y = self.position.y

        self.serverAddress = '169.254.79.197'
        self.port = 1053
        self.size = 1024
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.serverAddress,self.port))
        self.orientation = self.position.orientation
        self.shooting_part = ev3.LargeMotor('outC')
        self.shooting_part_right = ev3.LargeMotor('outD')
        self.shooting_part_left = ev3.LargeMotor('outA')
        self.elevation_part = ev3.LargeMotor('outB')
        self.loop = True
        self.flag = False
        self.A = False
        self.B = False
        self.C = False
        self.D = False
        self.elev_pos = 0
        

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
            self.position.move(left=-100, right=100, time=2)  
    # fonction pour tourner à gauche
    def turn_left_180(self):
        if self.loop == True:
            self.position.move(left=100, right=-100, time=2)

    def moving_pattern(self):
        compteur = 0
        #c'est ici qu'on va créer le pattern à l'aide de la fonction move de odemetrium en gardant la position connu
        while self.loop:
            # print(self.position.x , file = stderr)
            # print(self.position.y , file = stderr) 
            time.sleep(1)
            self.forward()
            self.turn_right_180()
            # print(self.position.x , file = stderr)
            # print(self.position.y , file = stderr)
            time.sleep(1)
            self.forward()
            self.turn_right_180()
            # print(self.position.x , file = stderr)
            # print(self.position.y , file = stderr)
            time.sleep(1)
            self.forward()
            self.turn_right_180()
            # print(self.position.x , file = stderr)
            # print(self.position.y , file = stderr)
            time.sleep(1)
            self.forward()
            self.turn_right_180()

        while self.loop==False:
            global block
            if block[6]==1:
                compteur = 0
            if block[6]!=1:
                compteur += 1            
            if compteur > 3:
                self.loop=True
                self.moving_pattern()
            # print("En dehors du moving loop", file = stderr)

            # pos = self.get_position()
            # print(pos)

    # def odometry_pattern(self):
    #     if self.A:
    #         continue
    #     if self.B:
    #         continue
    #     if self.C:
    #         continue
    #     if self.D:
    #         continue

    #on prend les information x, y et l'orientation qu'on va renvoyer en sortie de la fonction    
    def get_position(self):
        return self.x,self.y,self.orientation

    def ballistic_shooting(self,distance, pos):
        if pos > 0 and pos < 15:
            ball_dis = 0.0345*distance - 0.4000
            ball_dis = round(ball_dis)
            self.elevation_part.run_timed(time_sp=ball_dis * 1000, speed_sp=20)


    # def distance_calculation(self,w):
    #     #Regression linéaire avec les données dans le data.csv
    #     distance_estim = 3.9687 + (1194.9260/w)
    #     # size_px_init = 60
    #     # distance_init = 20
    #     print("#",int(w))
    #     spkr = Sound()
    #     spkr.speak('Distance calculated !')
    #     spkr.speak(int(distance_estim))
    #     # return (size_px_init*distance_init)/w
    #     return distance_estim

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
            time.sleep(1)
            # Request block
            bus.write_i2c_block_data(address, 0, data)
            # # Read block
            global block
            block = bus.read_i2c_block_data(address, 0, 20)
            # print("block 6 = ",block[6], "block 7 = ", block[7])
            
            if block[6]==1:
                # print("dedans")
                # Extract data
                sig = block[7]*256 + block[6]
                x = block[9]*256 + block[8]
                y = block[11]*256 + block[10]
                w = block[13]*256 + block[12]
                h = block[15]*256 + block[14]

                if y < 95:
                    self.loop = False
                    self.position.stop()
                    self.elevation_part.run_timed(time_sp=1 * 1000, speed_sp=20)
                    self.elev_pos = self.elev_pos - 1
                    
                elif y > 104:
                    self.loop = False
                    self.position.stop()
                    self.elevation_part.run_timed(time_sp=1 * 1000, speed_sp=-20)
                    self.elev_pos = self.elev_pos + 1 
                    
                else:
                    if x < 140:
                        self.loop = False

                        self.shooting_part_right.run_timed(time_sp=1 * 1000, speed_sp=40)
                        self.shooting_part_right.run_timed(time_sp=1 * 1000, speed_sp=-40)

                    elif x > 156:
                        self.loop = False

                        self.shooting_part_right.run_timed(time_sp=1 * 1000, speed_sp=-40)
                        self.shooting_part_right.run_timed(time_sp=1 * 1000, speed_sp=40)

                    else:
                        spkr = Sound()
                        self.loop = False
                        self.position.stop()
                        pos = self.get_position()
                        # spkr.speak('Target detected !')
                        # spkr.speak('Error calibration !')
                        # self.shooting_part_right.run_timed(time_sp=1 * 1000, speed_sp=40)
                        # self.shooting_part_right.run_timed(time_sp=1 * 1000, speed_sp=-40)

                        self.elevation_part.run_timed(time_sp=1 * 1000, speed_sp=20)
                        
                        # dis = self.distance_calculation(w)
                        # print("distance :", dis)
                        # print("largeur :", w)
                        dis = w
                        # print("hauteur :", h)
                        dis = int(dis)
                        dis = str(dis)
                        data1 = dis.encode("utf8")
                        self.s.send(data1)
                        self.shooting()

                        # self.loop = True
            else:
                sigs = 2
                data = [174, 193, 32, 2, sigs, 1]                    
                time.sleep(1)
                bus.write_i2c_block_data(address, 0, data)
                block = bus.read_i2c_block_data(address, 0, 20)

                sigs = 1
                data = [174, 193, 32, 2, sigs, 1]   

                if block[6]==2:
                    sig = block[7]*256 + block[6]
                    x = block[9]*256 + block[8]
                    y = block[11]*256 + block[10]
                    w = block[13]*256 + block[12]
                    h = block[15]*256 + block[14]

                    if y < 95:
                        self.loop = False
                        self.position.stop()
                        self.elevation_part.run_timed(time_sp=1 * 1000, speed_sp=20)
                        self.elev_pos = self.elev_pos - 1
                        
                    elif y > 104:
                        self.loop = False
                        self.position.stop()
                        self.elevation_part.run_timed(time_sp=1 * 1000, speed_sp=-20)
                        self.elev_pos = self.elev_pos + 1
                        
                    else:
                        if x < 140:
                            self.loop = False
                            self.position.stop()
                            self.shooting_part_right.run_timed(time_sp=1 * 1000, speed_sp=40)
                            self.shooting_part_right.run_timed(time_sp=1 * 1000, speed_sp=-40)

                        elif x > 156:
                            self.loop = False
                            self.position.stop()
                            self.shooting_part_right.run_timed(time_sp=1 * 1000, speed_sp=-40)
                            self.shooting_part_right.run_timed(time_sp=1 * 1000, speed_sp=40)

                        else:
                            spkr = Sound()
                            self.loop = False
                            self.position.stop()
                            pos = self.get_position()
                            # spkr.speak('Target detected !')
                            # spkr.speak('Error calibration !')
                            # self.shooting_part_right.run_timed(time_sp=1 * 1000, speed_sp=40)
                            # self.shooting_part_right.run_timed(time_sp=1 * 1000, speed_sp=-40)

                            self.elevation_part.run_timed(time_sp=1 * 1000, speed_sp=20)
                            # dis = self.distance_calculation(w)
                            # print("distance :", dis)
                            # print("largeur :", w)
                            dis = w
                            # print("hauteur :", h)
                            dis = int(dis)
                            dis = str(dis)
                            data1 = dis.encode("utf8")
                            self.s.send(data1)
                            self.shooting()        
                

    def shooting(self):
        # time.sleep(5000)
        while 1:
            data_shooting = self.s.recv(self.size)
            data_shooting = data_shooting.decode('utf8')
            print("detected")
            
            if data_shooting is not None:
                spk = Sound()
                # spk.speak('Order received !')   
                print("Shoot ",data_shooting, file = stderr)
                self.ballistic_shooting(int(data_shooting),self.elev_pos)
                self.shooting_part.run_timed(time_sp=3 * 1000, speed_sp=300)
                time.sleep(1)
                self.shooting_part.run_timed(time_sp=3 * 1000, speed_sp=-300)
                time.sleep(1)
                self.shooting_part.run_timed(time_sp=3 * 1000, speed_sp=300)
                time.sleep(1)
                self.shooting_part.run_timed(time_sp=3 * 1000, speed_sp=-300)
                data_shooting = None
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
    while True:
        bot.pixy_camera()
        time.sleep(3)


if __name__ == "__main__" :
    main()
