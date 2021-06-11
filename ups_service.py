#!/usr/bin/env python3
import struct
import smbus
import sys
import os
import time
import getopt
import RPi.GPIO as GPIO

class Service:

    def __init__(self, show_messaged, print_info):
        self.show_messaged = show_messaged
        self.print_info = print_info

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(4,GPIO.IN)
            
        self.bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
        self.address = 0x36
        self.bus.write_word_data(self.address, 0xfe, 0x0054)
        self.bus.write_word_data(self.address, 0x06, 0x4000)

    def read_voltage(self):
        "This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"
        read = self.bus.read_word_data(self.address, 0X02)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 1.25 /1000/16
        return voltage

    def read_capacity(self):
        "This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"
        read = self.bus.read_word_data(self.address, 0X04)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped/256
        return capacity

    def warn_about_shutdown(self):
        if not self.show_messaged:
            return

        os.system('wall "System going to power off - Low UPS battery... Powering down in 10 seconds."')

    def notify_cancel_shutdown(self):
        if not self.show_messaged:
            return

        os.system('wall "UPS-Plugged in - shutdown canceled."')

    def shutdown(self):
        os.system('sudo shutdown')

    def print_status(self, voltage, charge, pluggedIn):
        if not self.print_info:
            return

        status = "CHARGING"
        if not pluggedIn:
            status = "DISCHARGING"
        print("++++++++++++++++++++")
        print("Status: %s" % status)
        print("Voltage:%5.2fV" % voltage)
        print("Battery:%5i%%" % charge)
        print("++++++++++++++++++++")

    def run(self):
        while True:
            voltage = self.read_voltage()
            charge = self.read_capacity()
            pluggedIn = GPIO.input(4) == GPIO.HIGH
            
            if voltage == 0 or charge == 0:
                time.sleep(2)
                continue
                
            if not pluggedIn:
                if charge <= 20.0:
                    self.warn_about_shutdown()
                    time.sleep(10)
                    pluggedIn = GPIO.input(4) == GPIO.HIGH
                    if not pluggedIn:
                        self.shutdown()
                        break
                    else:
                        self.notify_cancel_shutdown()
                else:
                    self.print_status(voltage, charge, pluggedIn)
            else:
                self.print_status(voltage, charge, pluggedIn)

            time.sleep(2)
   
if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "v:", ["verbose="])

    verbosibility = 2
    for o, a in opts:
        if o in ("-v", "--verbose"):
            verbosibility = int(a)
    
    service = Service(verbosibility >= 1, verbosibility >= 2)
    service.run()