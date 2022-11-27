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
        self.hostAddress = '169.254.148.173' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
        self.port = 1050 # 3 is an arbitrary choice. However, it must match the port used by the client.
        self.backlog = 1
        self.size = 1024

    def server_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.hostAddress,self.port))
        #s.listen(self.backlog)
        self.s.listen()
        self.connexion_client, self.address = self.s.accept()

    def receive_distance(self):
        while 1:
            data = self.connexion_client.recv(self.size)

            if data:
                print(data)
                spkr = Sound()
                spkr.speak('Target detected')
                spkr.speak('Distance calculated')
                data = data.decode('utf8')
                data = int(data)
                spkr.speak(str(data))
                spkr.speak('You can shoot !')
                shoot = 'You can shoot'
                data_shoot = shoot.encode("utf8")
                self.s.send(data_shoot)
    



bot = Master_Bot()
#bot.sound()
bot.server_connection()
bot.receive_distance()
