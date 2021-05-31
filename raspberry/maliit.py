import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
servo1 = GPIO.PWM(7, 50)  # Note 3 is pin, 100 = 100Hz pulse
servo2 = GPIO.PWM(35, 50)
servo1.start(0)
servo2.start(1)

idText = open("/home/pi/Desktop/RPB/raspberry/servoDefID.txt", 'r+')
r = idText.read()



while True:
    t_ID = int(input("Enter id: "))
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
    servo1.ChangeDutyCycle(0)
servo1.stop()
GPIO.cleanup()
