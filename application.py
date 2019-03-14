import serial
import RPi.GPIO as GPIO
import threading
import random

# setup the GPIO pins / transceiver
IP = "70.150.145.199".encode()
teamMACS = ["5B-66-5A-D5-92-CC", "80-AB-14-FA-9F-A7"]
teamPASS = ["Password321", "Password123"]

selPin = 11
channelSel = 1

baud = 9600
bauds = [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]

regedDevices = list()
authDevices = list()

radio = threading.Semaphore(1)

def main():
    # set the GPIO mode
    GPIO.setmode(GPIO.BOARD)
    
    # init the serial interface
    ser = serial.Serial(port = '/dev/ttyAMA0')
    ser.baudrate = baud

    # start the randomization thread
    t = threading.Thread(target=randomize, args=(ser,))

    # start the broadcasting thread
    u = threading.Thread(target=broadcastIP, args=(ser,IP,))

    # start the receiver thread
    v = threading.Thread(target=receiver, args=(ser,))
    
    t.start()
    u.start()
    v.start()

    print("Finished Init\n\r")


# run the application
# example packet: 70.150.145.199|80-AB-14-FA-9F-A7|Password123|Hello
def receiver(ser):
    while(1):
        radio.acquire()
        data = ser.readline()
        radio.release()
        data = data.decode().split("|")
   
        # check that the IP of this packet belongs to this node
        if(data[0] != IP):
            print("This packet belongs to IP: " + data[0] + "\n\r")
            continue
    
        print("This packet belongs to this node\n")
        
        # check that the MAC address is in the list of team MACs
        if(data[1] not in teamMACS):
            print("This is not a valid MAC address\n\r")
            radio.acquire()
            ser.write("INV_MAC:" + data[1] + "\n")
            radio.release()
            continue
        
        # check if the device has been authenticated before
        if(data[1] not in authDevices):
            print("Authenticating Device\n")
            if(data[2] in teamPASS):
                print("Authenticating device: " + data[1] + "\n\r")
                #ser.write("reg_dev:" + data[1] + "\n")
                authDevices.append(data[1])
            else:
                ser.write("AUTH_FAIL:")
                continue
        else:
            print("This device has been authenticated\n\r")
            ser.write("reg_dev:AUTH_VAL\n")

        parseCommand(data[3])



def broadcastIP(serialObj, IP):
    radio.acquire()
    serialObj.write(IP)
    radio.release()
    print("Broadcasted my IP\n\r", flush=True)
    sleep(1)


def parseCommand(cmd):
    if(cmd == "Hello"):
        radio.acquire()
        ser.write("cmd:Hello from HC-12\n\r", flush=True)
        radio.release()


def randomize(ser):
    while(1):
        print("Randomizing...\n\r", flush=True)
        #generate random baud and broadcast channel
        channel = channelSel * random.randint(0,20)
        baud = bauds[random.randint(0,7)]
        
        #setup the GPIO 
        GPIO.setup(selPin, GPIO.OUT)    # set the GPIO pin of transceiver select
        GPIO.output(selPin, GPIO.LOW)   # set the GPIO pin to enable commands on hc12
        
        #write to the HC-12 in command mode
        radio.acquire()
        ser.write("AT+C" + str(channel))
        ser.write("AT+B" + str(baud))

        #change the raspi baud rate
        ser.baudrate = baud
        radio.release()
    
        #clean up the GPIO port
        GPIO.cleanup()

        if(channel + 1 == 4):
            channel = 1
        else:
            channel = channel + 1

        print("Finished randomizing, sleeping...\n\r", flush=True)
        sleep(60)


if __name__ == "__main__":
    main()
