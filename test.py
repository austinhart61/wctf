#!/usr/bin/env python3
import time
import serial
import threading
import argparse
import RPi.GPIO as GPIO

ser = serial.Serial(

	port='/dev/serial0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
    )

counter=0
IP = "192.215.16.754\n"

radio = threading.Lock()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="the IP address of this node", default="")
    parser.add_argument("-b", "--baud", help="initial baud rate of the node, likely to change with the randomizer", default=9600, type=int)
    args = parser.parse_args()
    
    IP = args.ip
    baud = args.baud
    
    GPIO.setmode(GPIO.BOARD)
    
    t = threading.Thread(target=receive)
    u = threading.Thread(target=broadcast)
    t.start()
    u.start()
    t.join()
    u.join()
    while 1:
        time.sleep(.5)
    #while 1:
    #x=ser.readline()
    #c=x.decode().split("|")
    #if len(c) > 1:
    #    print(c)
    #    broadcast()


def broadcast():
    while(1):
        radio.acquire()
        print("broadcasting")
        ser.write(IP)
        radio.release()
        time.sleep(1)


def receive():
    print("Receiving")
    time.sleep(2)


if __name__ == "__main__":
    main()
