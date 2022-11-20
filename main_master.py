import os
import sys
import time
import socket
from ev3dev2.sound import Sound

from threading import Thread


#Faire une classe Slave Robot en prenant toutes les fonction du dessous
class Master_Bot():
    def __init__(self):
        
        self.hostMACAddress = '169.254.116.31' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
        self.port = 1050 # 3 is an arbitrary choice. However, it must match the port used by the client.
        self.backlog = 1
        self.size = 1024

    def server_connection(self):
        s = socket.socket()
        s.bind((self.hostMACAddress,self.port))
        s.listen(self.backlog)
        client, address = s.accept()

    def receive_distance(self):
        while 1:
        
            data = client.recv(size)
            if data:
                print(data)
                spkr = Sound()

                spkr.speak('Distance calculated !')




bot = Master_Bot()
bot.server_connection()
bot.receive_distance()
