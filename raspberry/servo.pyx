# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and set servo1 as pin 11 as PWM
GPIO.setup(7, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
servo1 = GPIO.PWM(7, 50)  # Note 3 is pin, 100 = 100Hz pulse
servo2 = GPIO.PWM(35, 50)

#100 hz: 5 = 360, 7 = 270, 8.5 = 180, 10 = 90,
#(low power) 22 = -90, 23= -180, 24 = -270, 25 =  -360,

idText = open("/home/pi/Desktop/RPB/raspberry/servoDefID.txt", 'r+')
r = idText.read()

def trashDump(t_ID):
    #start PWM running, but with value of 0 (pulse off)
    servo1.start(0)
    servo2.start(1)
    global r
    if r == "A":
        r = caseA(t_ID)
    elif r == "B":
        r = caseB(t_ID)
    elif r == "C":
        r = caseC(t_ID)
    elif r == "D":
        r = caseD(t_ID)
    servo1.ChangeDutyCycle(0)
    idText = open("/home/pi/Desktop/RPB/raspberry/servoDefID.txt", 'w')
    idText.writelines(r)
    idText.close()
    servo2.ChangeDutyCycle(7) # 12 or 7 neutral position
    time.sleep(1)
    servo2.ChangeDutyCycle(2) # right +90 deg position
    time.sleep(1)

    servo2.ChangeDutyCycle(0)
    print("Goodbye!")

def caseA(t_ID):
    global r
    if t_ID == 1:
        print("Rotate 0 degree")
        servo1.ChangeDutyCycle(0)
        time.sleep(2)
        r = "A"
    elif t_ID == 2:
        print("Rotate 90 degrees")
        servo1.ChangeDutyCycle(2) # right +90 deg position
        time.sleep(.44)
        r = "B"
    elif t_ID == 3:
        print("Rotate 180 degrees")
        servo1.ChangeDutyCycle(2) # right +180 deg position
        time.sleep(.81) #9 or 8
        r = "C"
    elif t_ID == 4:
        print("Rotate -90 degrees")
        servo1.ChangeDutyCycle(12)
        time.sleep(.71) #7 or 8 -90 deg
        r = "D"
    print("Case A")
    return r


def caseB(t_ID):
    global r
    if t_ID == 1:
        print("Rotate -90 degree")
        servo1.ChangeDutyCycle(12)
        time.sleep(.71) #7 or 8 -90 deg
        r = "A"
    elif t_ID == 2:
        print("Rotate 0 degrees")
        servo1.ChangeDutyCycle(0)
        time.sleep(2)
        r = "B"
    elif t_ID == 3:
        print("Rotate 90 degrees")
        servo1.ChangeDutyCycle(2) # right +90 deg position
        time.sleep(.44)
        r = "C"
    elif t_ID == 4:
        print("Rotate 180 degrees")
        servo1.ChangeDutyCycle(2) # right +180 deg position
        time.sleep(.81) #9 or 8
        r = "D"
    print("Case B")
    return r


def caseC(t_ID):
    global r
    if t_ID == 1:
        print("Rotate 180 degree")
        servo1.ChangeDutyCycle(2) # right +180 deg position
        time.sleep(.81) #9 or 8
        r = "A"
    elif t_ID == 2:
        print("Rotate -90 degrees")
        servo1.ChangeDutyCycle(12)
        time.sleep(.71) #7 or 8 -90 deg
        r = "B"
    elif t_ID == 3:
        print("Rotate 0 degrees")
        servo1.ChangeDutyCycle(0)
        time.sleep(2)
        r = "C"
    elif t_ID == 4:
        print("Rotate 90 degrees")
        servo1.ChangeDutyCycle(2) # right +90 deg position
        time.sleep(.44)
        r = "D"
    print("Case C")
    return r


def caseD(t_ID):
    global r
    if t_ID == 1:
        print("Rotate 90 degree")
        servo1.ChangeDutyCycle(2) # right +90 deg position
        time.sleep(.44)
        r = "A"
        return r
    elif t_ID == 2:
        print("Rotate 180 degrees")
        servo1.ChangeDutyCycle(2) # right +180 deg position
        time.sleep(.81) #9 or 8
        r = "B"
    elif t_ID == 3:
        print("Rotate -90 degrees")
        servo1.ChangeDutyCycle(12)
        time.sleep(.71) #7 or 8 -90 deg
        r = "C"
    elif t_ID == 4:
        print("Rotate 0 degrees")
        servo1.ChangeDutyCycle(0)
        time.sleep(2)
        r = "D"
    print("Case D")
    return r


#while True:
#    t_ID = int(input("enter id: "))
#    trashDump(t_ID)