#import raspberry.sendAlert as sAlert

#import sendAlert as sAlert
import RPi.GPIO as GPIO
import MySQLdb
import time
import sys
sys.path.append('/home/pi/Desktop/RPB')
import app

sensor = 37
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)

#Connection to database
def connection():
    conn = MySQLdb.connect(host="localhost",
                           user="rex",
                           passwd="pi",
                           db="rpb")
    c = conn.cursor()
    return c, conn

print("In setup...\n")

try:
    r = 0
    while True:
        x, conn = connection()
        if GPIO.input(sensor):
            stat = "not"
            print("NOT Full")
            x.execute("UPDATE rpbInfo SET status = %s", (stat,))
            conn.commit()
            while GPIO.input(sensor):
                time.sleep(5) #every 10 seconds capture obstacle
        else:
            print("FULL")
            time.sleep(5) # 60 seconds wait for recapture obstacle
            r += 1
            if r > 2:
                stat = "full"
                now = "now"
                print("Send MSG")
                x.execute("UPDATE rpbInfo SET lastSent = CURRENT_TIMESTAMP")
                x.execute("UPDATE rpbInfo SET status = %s", (stat,))
                conn.commit()
                app.stmsg = False
                #sAlert.warn_message()
                #sAlert.pushBulletAlert()
except KeyboardInterrupt:
    GPIO.cleanup()