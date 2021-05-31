# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

#100 hz: 5 = 360, 7 = 270, 8.5 = 180, 10 = 90,
#(low power) 22 = -90, 23= -180, 24 = -270, 25 =  -360,
# Set pin 11 as an output, and set servo1 as pin 11 as PWM
#GPIO.setup(37, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
#servo1 = GPIO.PWM(37, 50)  # Note 3 is pin, 100 = 100Hz pulse
servo2 = GPIO.PWM(35, 50)
def trashDump(t_ID):
    servo2.start(1)
    if t_ID == 2:
        # 2 biodegradable
        motor(150)
    elif t_ID == 3:
        #3 none biodegradable
        motor(88)
    else:
        #4 recyclable
        servo2.ChangeDutyCycle(7) # 12 or 7 neutral position
        time.sleep(1)
        servo2.ChangeDutyCycle(2) # right +90 deg position
        time.sleep(1)

    servo2.ChangeDutyCycle(0)
    print("Goodbye!")

control_pins = [7,11,13,15]
for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1],

]

halfstep_seq2 = [
  [1,0,0,1],
  [0,0,0,1],
  [0,0,1,1],
  [0,0,1,0],
  [0,1,1,0],
  [0,1,0,0],
  [1,1,0,0],
  [1,0,0,0],

]

def motor(a):

    for i in range(a): #140 FULLL //HALF 90 80
      for halfstep in range(8):
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.001)
    time.sleep(1)
    servo2.ChangeDutyCycle(7) # 12 or 7 neutral position
    time.sleep(1)
    servo2.ChangeDutyCycle(2) # right +90 deg position
    time.sleep(1)


    for i in range(a):
      for halfstep in range(8):
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep_seq2[halfstep][pin])
        time.sleep(0.001)

#motor(150)

#trashDump(2)
#trashDump(3)
while True:
    num = int(input("Enter id [2 Bio, 3 non-Bio, 4 recy]: "))
    trashDump(num)