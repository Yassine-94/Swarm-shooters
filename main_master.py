#!/usr/bin/env python3 
import os
import sys
import time
import socket
from ev3dev2.sound import Sound

from threading import Thread


#Faire une classe Slave Robot en prenant toutes les fonction du dessous
class Master_Bot():
    def __init__(self):
        self.hostAddress = '169.254.137.211' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
        self.port = 1050 # 3 is an arbitrary choice. However, it must match the port used by the client.
        self.backlog = 1
        self.size = 1024

    def server_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.hostAddress,self.port))
        #s.listen(self.backlog)
        self.s.listen()
        self.connexion_client, self.address = self.s.accept()

    def distance_calculation(self,w):
        #Regression linéaire avec les données dans le data.csv
        distance_estim = 3.9687 + (1194.9260/w)
        # size_px_init = 60
        # distance_init = 20
        print("#",int(w))
        spkr = Sound()
        spkr.speak('Distance calculated !')
        spkr.speak(int(distance_estim))
        # return (size_px_init*distance_init)/w
        return distance_estim

    def receive_distance(self):
        # set_font('Lat15-Terminus24x12')
        while 1:
            data = self.connexion_client.recv(self.size)

            if data:
                print(data)
                spkr = Sound()
                spkr.speak('Target detected')
                # spkr.speak('Distance calculated')
                data = data.decode('utf8')
                data = int(data)
                spkr.speak(str(data))
                
                # shoot = 'You can shoot'
                # data_shoot = shoot.encode("utf8")
                dis = self.distance_calculation(data)
                print("distance :", dis)
                
                # print("hauteur :", h)
                dis = int(dis)
                dis = str(dis)
                spkr.speak('You can shoot !')
                data_shoot = dis.encode("utf8")
                print(data_shoot)
                self.connexion_client.send(data_shoot)
                # try:
                #     self.s.send(data_shoot)
                # except:
                #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                # finally:
                #     print("No EZrror")
                self.receive_distance()
    



bot = Master_Bot()
#bot.sound()
bot.server_connection()
bot.receive_distance()
