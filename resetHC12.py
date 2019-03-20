#!/usr/bin/env python3

import serial
import RPi.GPIO as GPIO

# all the possible baud rates
bauds = [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]

# setup the serial port to the HC12
ser = serial.Serial(port='/dev/serial0', baudrate = 9600, timeout = 1)

# setup the GPIO on the raspi
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

# enable command mode on the HC12
GPIO.output(11, GPIO.LOW)

index = 3

#begin scanning bauds
while 1:
    ser.write("AT+DEFAULT")
    response = ser.readline()
    if(response == "OK+DEFAULT\r\n"):
        print("reset at baud: " + str(bauds[index]))
        break
    else:
        ser.baudrate = bauds[index]
        index = (index + 1) % 8
        print("trying next baud: " + str(bauds[index]))

GPIO.cleanup()


