#!/usr/bin/env pybricks-micropython
'''Hello to the world from ev3dev.org'''

import os
import sys
import time
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Port



def main():
    '''The main function of our program'''

    ev3 = EV3Brick()
    # moteur

    #test_motor.run_until_stalled(500) tourne à l'infini jusqu'à forcer l'arrêt
    while (True):
        touch = TouchSensor(Port.S1) #we add a touch sensor
        if touch.pressed():#if the touch sensor is pressed then...
            test_motor = Motor(Port.C) #... we define a variable for the motor at port C and...
            test_motor.run_target(500, 180) #... we make a rotation of the motor because the touch sensor has been pressed

    #son
    """
    ev3.speaker.beep(frequency=1000, duration=500)
    ev3.speaker.beep(frequency=800, duration=200)
    ev3.speaker.beep(frequency=1000, duration=500)
    ev3.speaker.beep(frequency=800, duration=200)
    """

    #ev3.speaker.beep()

if __name__ == "__main__" :
    main()
