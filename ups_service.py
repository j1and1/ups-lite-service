#!/usr/bin/env python3
import struct
import smbus
import sys
import os
import time
import RPi.GPIO as GPIO

def readVoltage(bus):
    "This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"
    address = 0x36
    read = bus.read_word_data(address, 0X02)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    voltage = swapped * 1.25 /1000/16
    return voltage


def readCapacity(bus):
    "This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"
    address = 0x36
    read = bus.read_word_data(address, 0X04)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    capacity = swapped/256
    return capacity

def QuickStart(bus):
    address = 0x36
    bus.write_word_data(address, 0x06,0x4000)
      

def PowerOnReset(bus):
    address = 0x36
    bus.write_word_data(address, 0xfe,0x0054)

def WarnAboutShutdown():
    os.system('wall "System going to power off - Low UPS battery... Powering down in 10 seconds."')

def NotifyCancelShutdown():
    os.system('wall "UPS-Plugged in - Shutdown canceled."')

def Shutdown():
    os.system('sudo shutdown')

def printStatus(voltage, charge, pluggedIn):
    status = "CHARGING"
    if not pluggedIn:
        status = "DISCHARGING"
    print("++++++++++++++++++++")
    print("Status: %s" % status)
    print("Voltage:%5.2fV" % voltage)
    print("Battery:%5i%%" % charge)
    print("++++++++++++++++++++")
   
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN)
       
bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

PowerOnReset(bus)
QuickStart(bus)

while True:
    voltage = readVoltage(bus)
    charge = readCapacity(bus)
    pluggedIn = GPIO.input(4) == GPIO.HIGH
    
    if voltage == 0 or charge == 0:
        time.sleep(2)
        continue
        
    if not pluggedIn:
        if charge <= 20.0:
            WarnAboutShutdown()
            time.sleep(10)
            pluggedIn = GPIO.input(4) == GPIO.HIGH
            if not pluggedIn:
                Shutdown()
            else:
                NotifyCancelShutdown()
        else:
            printStatus(voltage, charge, pluggedIn)
    else:
        printStatus(voltage, charge, pluggedIn)

    time.sleep(2)
