#!/usr/bin/env python3

import serial
import RPi.GPIO as GPIO
import threading
import random
import time
import argparse

# setup the GPIO pins / transceiver
IP = "1.2.3.4"
teamMACS = ["5B-66-5A-D5-92-CC", "80-AB-14-FA-9F-A7"]
teamPASS = ["Password321", "Password123"]

selPin = 11
channelSel = 20

baud = 9600
bauds = [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]

randoEnable = 1
randoDelay = 300

regedDevices = list()
authDevices = list()

# init the serial interface
ser = serial.Serial(

	port='/dev/serial0',
	baudrate = baud,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
    )

radio = threading.Lock()

def main():
    global IP
    global selPin
    global channelSel
    global baud
    global randoEnable
    global randoDelay

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="the IP address of this node", default="")
    parser.add_argument("-s", "--select", help="Raspi select pin for the HC12", default=11, type=int)
    parser.add_argument("-c", "--channel", help="select the scheduler for the channel that this node will run on", default=20, type=int)
    parser.add_argument("-b", "--baud", help="initial baud rate of the node, likely to change with the randomizer", default=9600, type=int)
    parser.add_argument("-r", "--rando", help="enable the randomizer on this node", default=0, type=int)
    parser.add_argument("-d", "--delay", help="the time (seconds) to delay randomizing on this node", default=300, type=int)
    args = parser.parse_args()
    
    IP = args.ip
    selPin = args.select
    channelSel = args.channel
    baud = args.baud
    randoEnable = args.rando
    randoDelay = args.delay

    # set the GPIO mode
    GPIO.setmode(GPIO.BOARD)
    
    # start the randomization thread
    t = threading.Thread(target=randomize)

    # start the broadcasting thread
    u = threading.Thread(target=broadcastIP)

    # start the receiver thread
    v = threading.Thread(target=receiver)
    
    t.start()
    u.start()
    v.start()

    t.join()
    u.join()
    v.join()

    print("Finished Init\n\r")
    while(1):
        time.sleep(.5)


# run the application
# example packet: 70.150.145.199|80-AB-14-FA-9F-A7|Password123|Hello
def receiver():
    print("Running receiver thread\n")
    while(1):
        time.sleep(2)
        radio.acquire()
        data = ser.readline()
        radio.release()
        data = data.decode().split("|")
        
        # check that the IP of this packet belongs to this node
        if(data[0] == IP):
            print("This packet belongs to this node\n")
        elif(data[0] != IP):
            print("This packet belongs to IP: " + data[0] + "\n\r")
            continue
        else:
            continue
        
        # check that the MAC address is in the list of team MACs
        try:
            if(data[1] not in teamMACS):
                print("This is not a valid MAC address\n\r")
                radio.acquire()
                ser.write("INV_MAC:" + data[1] + "\n")
                radio.release()
                continue
        except IndexError:
            print("Incomplete packet structure detected")
            continue

        # check if the device has been authenticated before
        if(data[1] not in authDevices):
            print("Authenticating Device\n")
            if(data[2] in teamPASS):
                print("Authenticating device: " + data[1] + "\n\r")
                ser.write("reg_dev:" + data[1] + "\n")
                authDevices.append(data[1])
            else:
                #ser.write("AUTH_FAIL:")
                continue
        else:
            print("This device has been authenticated\n\r")
            #ser.write("reg_dev:AUTH_VAL\n")

        parseCommand(data[3])



def broadcastIP():
    print("Running broadcast thread\n")
    global IP, ser
    while(1):
        print("Broadcasting")
        radio.acquire()
        ser.write(IP+'\n')
        radio.release()
        print("Broadcasted my IP\r\n")
        time.sleep(2)


def parseCommand(cmd):
    if(cmd == "Hello"):
        radio.acquire()
        ser.write("cmd:Hello from HC-12\n\r")
        radio.release()


def randomize():
    print("Running rando thread\n")
    global channelSel
    while(randoEnable):
        print("Randomizing...\n\r")
        #generate random baud and broadcast channel
        channel = channelSel + random.randint(0,20)
        baud = bauds[random.randint(0,7)]
        print("New settings:\n Baud: " + str(baud) + "\nChannel: " + str(channel))

        #setup the GPIO
        GPIO.setup(selPin, GPIO.OUT)    # set the GPIO pin of transceiver select
        GPIO.output(selPin, GPIO.LOW)   # set the GPIO pin to enable commands on hc12

        #write to the HC-12 in command mode
        #print("Acquiring lock for randomizer")
        radio.acquire()
        #print("Acquired lock for randomizer")
        ser.write("AT+C" + str(channel))
        ser.write("AT+B" + str(baud))

        #change the raspi baud rate
        ser.baudrate = baud
        #print("Releasing lock for randomizer")
        radio.release()
    
        #clean up the GPIO port
        GPIO.output(selPin, GPIO.HIGH)

        if(channelSel + 20 == 80):
            channelSel = 20
        else:
            channelSel = channelSel + 20

        print("Finished randomizing, sleeping...\n\r")
        time.sleep(randoDelay)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
