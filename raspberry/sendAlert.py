from pushbullet import Pushbullet
from twilio.rest import Client
import MySQLdb
import time
import os

#Define your Twilio credentials
account_sid = 'AC6a83a2245b864deaaf8d022229cb282a'
auth_token = '352d0438dde9b628110bc51aa53227d4'

client = Client(account_sid, auth_token)

#create connection to database
def connecMe():
    conn = MySQLdb.connect(host="localhost",
                           user="rex",
                           passwd="pi",
                           db="rpb")
    c = conn.cursor()
    return c, conn

# Get database data
c, conn = connecMe()
c.execute("SELECT stablishment, phoneNo FROM rpbInfo")
rInfo = c.fetchone()
loc = rInfo[0]
reciever = rInfo[1]

def warn_message():
    client.messages.create(
    to='+639771506700',
    from_='+15593435018',
    body="Alert! Please check the trash cans to check if it's full.")
#warn_message()

def pushBulletAlert():
    pb = Pushbullet("o.59mr6fXSTZCg4qBhJd9yzacxGrWJr1B9")
    print(pb.devices)
    #print(reciever)
    dev = pb.get_device(reciever)
    push = dev.push_note("Alert!!", "Please check the trash cans might be already full.")
    dev = pb.get_device("Vivo Vivo 1609")
    push = dev.push_note("Alert!!", "Please check the trash cans might be already full.")
    time.sleep(1)

pushBulletAlert()
