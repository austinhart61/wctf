import serial
import RPi.GPIO as GPIO

# setup the GPIO pins / transceiver
IP = "70.150.145.199"
selPin = 11
baud = 9600
regedDevices = list()
authDevices = list()
teamMACS = ["5B-66-5A-D5-92-CC", "80-AB-14-FA-9F-A7"]
teamPASS = ["Password321", "Password123"]

def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(selPin, GPIO.OUT)    # set the GPIO pin of transceiver select
    GPIO.output(selPin, GPIO.LOW)   # set the GPIO pin to enable commands on hc12

    ser = serial.Serial(port = '/dev/ttyAMA0')
    ser.baudrate = baud

    print("Finished Init\n")

    # run the application
    # example packet: 70.150.145.199|80-AB-14-FA-9F-A7|Password123|Hello
    while(1):
        broadcastIP(ser)
        data = ser.readline()
        data = data.decode().split("|")
   
        # check that the IP of this packet belongs to this node
        if(data[0] != IP):
            print("This packet belongs to IP: " + data[0] + "\n")
            continue
    
        print("This packet belongs to this node\n")
        
        # check that the MAC address is in the list of team MACs
        if(data[1] not in teamMACS):
            print("This is not a valid MAC address\n")
            ser.write("reg_dev:INV_MAC\n")
            continue
        
        # check if the device has been authenticated before
        if(data[1] not in authDevices):
            print("Authenticating Device\n")
            if(data[2] in teamPASS):
                print("Authenticating device: " + data[1] + "\n")
                ser.write("reg_dev:" + data[1] + "\n")
                authDevices.append(data[1])
            else:
                ser.write("reg_dev:AUTH_FAIL")
                continue
        else:
            print("This device has been authenticated\n")
            ser.write("reg_dev:AUTH_VAL\n")

        parseCommand(data[3])
    

def broadcastIP(serialObj):
    serialObj.write(IP)
    print("Broadcasted my IP\n")
    sleep(1)


def parseCommand(cmd):
    if(cmd == "Hello"):
        ser.write("cmd:Hello from HC-12\n")

if __name__ == "__main__":
    main()
