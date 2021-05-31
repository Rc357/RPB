# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

#100 hz: 5 = 360, 7 = 270, 8.5 = 180, 10 = 90,
#(low power) 22 = -90, 23= -180, 24 = -270, 25 =  -360,

def trashDump(t_ID):
    # Set pin 11 as an output, and set servo1 as pin 11 as PWM
    GPIO.setup(37, GPIO.OUT)
    GPIO.setup(35, GPIO.OUT)
    servo1 = GPIO.PWM(37, 50)  # Note 3 is pin, 100 = 100Hz pulse
    servo2 = GPIO.PWM(35, 50)

    #start PWM running, but with value of 0 (pulse off)
    servo1.start(0)
    servo2.start(1)
    
    servo1.ChangeDutyCycle(12) # 12 or 7 neutral position
    time.sleep(1)
    servo1.ChangeDutyCycle(2) # right +90 deg position
    time.sleep(1)
    servo1.ChangeDutyCycle(0) 
    if t_ID == 2:
        # 2 biodegradable
        motor(500)
        servo2.ChangeDutyCycle(7) # 12 or 7 neutral position
        time.sleep(1)
        servo2.ChangeDutyCycle(2) # right +90 deg position
        time.sleep(1)
        servo2.ChangeDutyCycle(0)
        motor(-500)
    elif t_ID == 3:
        #3 none biodegradable
        motor(300)
        servo2.ChangeDutyCycle(7) # 12 or 7 neutral position
        time.sleep(1)
        servo2.ChangeDutyCycle(2) # right +90 deg position
        time.sleep(1)
        servo2.ChangeDutyCycle(0)
        motor(-300)
    elif t_ID == 4:
        #4 recyclable
        servo2.ChangeDutyCycle(7) # 12 or 7 neutral position
        time.sleep(1)
        servo2.ChangeDutyCycle(2) # right +90 deg position
        time.sleep(1)
        servo2.ChangeDutyCycle(0)
    else:
        servo2.ChangeDutyCycle(7) # 12 or 7 neutral position
        time.sleep(1)
        servo2.ChangeDutyCycle(2) # right +90 deg position
        time.sleep(1)
        servo2.ChangeDutyCycle(0)
    
    servo1.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)
    print("Goodbye!")


def motor(a):
    out1 = 7
    out2 = 11
    out3 = 13
    out4 = 15

    GPIO.setup(out1,GPIO.OUT)
    GPIO.setup(out2,GPIO.OUT)
    GPIO.setup(out3,GPIO.OUT)
    GPIO.setup(out4,GPIO.OUT)
    i=0
    positive=0
    negative=0
    y=0
    GPIO.output(out1,GPIO.LOW)
    GPIO.output(out2,GPIO.LOW)
    GPIO.output(out3,GPIO.LOW)
    GPIO.output(out4,GPIO.LOW)
    x = int(a)
    if x>0 and x<=500:
      for y in range(x,0,-1):
          if negative==1:
              if i==7:
                  i=0
              else:
                  i=i+1
              y=y+2
              negative=0
          positive=1
          #print((x+1)-y)
          if i==0:
              GPIO.output(out1,GPIO.HIGH)
              GPIO.output(out2,GPIO.LOW)
              GPIO.output(out3,GPIO.LOW)
              GPIO.output(out4,GPIO.LOW)
              time.sleep(0.03)
              #time.sleep(1)
          elif i==1:
              GPIO.output(out1,GPIO.HIGH)
              GPIO.output(out2,GPIO.HIGH)
              GPIO.output(out3,GPIO.LOW)
              GPIO.output(out4,GPIO.LOW)
              time.sleep(0.03)
              #time.sleep(1)
          elif i==2:  
              GPIO.output(out1,GPIO.LOW)
              GPIO.output(out2,GPIO.HIGH)
              GPIO.output(out3,GPIO.LOW)
              GPIO.output(out4,GPIO.LOW)
              time.sleep(0.03)
              #time.sleep(1)
          elif i==3:    
              GPIO.output(out1,GPIO.LOW)
              GPIO.output(out2,GPIO.HIGH)
              GPIO.output(out3,GPIO.HIGH)
              GPIO.output(out4,GPIO.LOW)
              time.sleep(0.03)
              #time.sleep(1)
          elif i==4:  
              GPIO.output(out1,GPIO.LOW)
              GPIO.output(out2,GPIO.LOW)
              GPIO.output(out3,GPIO.HIGH)
              GPIO.output(out4,GPIO.LOW)
              time.sleep(0.03)
              #time.sleep(1)
          elif i==5:
              GPIO.output(out1,GPIO.LOW)
              GPIO.output(out2,GPIO.LOW)
              GPIO.output(out3,GPIO.HIGH)
              GPIO.output(out4,GPIO.HIGH)
              time.sleep(0.03)
              #time.sleep(1)
          elif i==6:    
              GPIO.output(out1,GPIO.LOW)
              GPIO.output(out2,GPIO.LOW)
              GPIO.output(out3,GPIO.LOW)
              GPIO.output(out4,GPIO.HIGH)
              time.sleep(0.03)
              #time.sleep(1)
          elif i==7:    
              GPIO.output(out1,GPIO.HIGH)
              GPIO.output(out2,GPIO.LOW)
              GPIO.output(out3,GPIO.LOW)
              GPIO.output(out4,GPIO.HIGH)
              time.sleep(0.03)
              #time.sleep(1)
          if i==7:
              i=0
              continue
          i=i+1


    elif x<0 and x>=-500:
      x=x*-1
      for y in range(x,0,-1):
          if positive==1:
              if i==0:
                  i=7
              else:
                  i=i-1
              y=y+3
              positive=0
          negative=1
          #print((x+1)-y) 
          if i==0:
              GPIO.output(out1,GPIO.HIGH)
              GPIO.output(out2,GPIO.LOW)
              GPIO.output(out3,GPIO.LOW)
              GPIO.output(out4,GPIO.LOW)
              time.sleep(0.03)
              #time.sleep(1)
          elif i==1:
              GPIO.output(out1,GPIO.HIGH)
              GPIO.output(out2,GPIO.HIGH)
              GPIO.output(out3,GPIO.LOW)
              GPIO.output(out4,GPIO.LOW)
              time.sleep(0.03)
              #time.sleep(1)
          elif i==2:  
              GPIO.output(out1,GPIO.LOW)
              GPIO.output(out2,GPIO.HIGH)
              GPIO.output(out3,GPIO.LOW)
              GPIO.output(out4,GPIO.LOW)
              time.sleep(0.03)
              #time.sleep(1)
          elif i==3:    
              GPIO.output(out1,GPIO.LOW)
              GPIO.output(out2,GPIO.HIGH)
              GPIO.output(out3,GPIO.HIGH)
              GPIO.output(out4,GPIO.LOW)
              time.sleep(0.03)
              #time.sleep(1)
          elif i==4:  
              GPIO.output(out1,GPIO.LOW)
              GPIO.output(out2,GPIO.LOW)
              GPIO.output(out3,GPIO.HIGH)
              GPIO.output(out4,GPIO.LOW)
              time.sleep(0.03)
              #time.sleep(1)
          elif i==5:
              GPIO.output(out1,GPIO.LOW)
              GPIO.output(out2,GPIO.LOW)
              GPIO.output(out3,GPIO.HIGH)
              GPIO.output(out4,GPIO.HIGH)
              time.sleep(0.03)
              #time.sleep(1)
          elif i==6:    
              GPIO.output(out1,GPIO.LOW)
              GPIO.output(out2,GPIO.LOW)
              GPIO.output(out3,GPIO.LOW)
              GPIO.output(out4,GPIO.HIGH)
              time.sleep(0.03)
              #time.sleep(1)
          elif i==7:    
              GPIO.output(out1,GPIO.HIGH)
              GPIO.output(out2,GPIO.LOW)
              GPIO.output(out3,GPIO.LOW)
              GPIO.output(out4,GPIO.HIGH)
              time.sleep(0.03)
              #time.sleep(1)
          if i==0:
              i=7
              continue
          i=i-1 
#motor(-500)
while True:
    s = int(input("Enter "))
    trashDump(s)
GPIO.cleanup()
