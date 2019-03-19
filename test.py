#!/usr/bin/env python3

import time
import serial
import requests

ser = serial.Serial(

	port='/dev/serial0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
    )

counter=0
stringtest = "Hello from raspi"

def broadcast():
    ser.write(stringtest)
    time.sleep(1)


def main():
    while 1:
    #x=ser.readline()
    #c=x.decode().split("|")
    #if len(c) > 1:
    #    print(c)
        broadcast()

if __name__ == "__main__":
    main()
