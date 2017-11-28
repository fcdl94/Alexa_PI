#!/usr/bin/env python

# Copyright (c) Franzo' Damiano 2017
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import Adafruit_PCA9685 as pca
import time

class servomanager:
    def __init__(self,input_address,bus_number):
        self.pwm=pca.PCA9685(address=input_address,busnum=bus_number)
        self.pwm.set_pwm_freq(60)
        self.servo_min=150
        self.servo_max=600
    def movto(self,position):
        if(position==1):
            self.pwm.set_pwm(0, 0, self.servo_min)
            time.sleep(1)
        if(position==2):
            self.pwm.set_pwm(0,0,(self.servo_min+self.servo_max)/2)
            time.sleep(1)
        else:
            self.pwm.set_pwm(0,0,self.servo_max)
            time.sleep(1)

#esempio funzionamento
#servo=servomanager(0x54,1)
#servo.movto(1)
#servo.movto(3)
##servo.movto(2)
##servo.movto(3)
#servo.movto(1)
