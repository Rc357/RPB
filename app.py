# -*- coding: utf-8 -*-
from flask import *
import raspberry.detectAndPredect as dap
import MySQLdb
import os

app = Flask(__name__)
app.secret_key = "recycle-pi-bin"


#Connection to database
def connection():
    conn = MySQLdb.connect(host="localhost",
                           user="rex",
                           passwd="pi",
                           db="rpb")
    c = conn.cursor()
    return c, conn

# Get database data
c, conn = connection()
c.execute("SELECT stablishment, phoneNo, lastSent FROM rpbInfo")
infoResult = c.fetchone()
c.execute("SELECT name, password FROM user")
myresult = c.fetchone()
# stored data to variables
stab = infoResult[0]
num = infoResult[1]
sent = infoResult[2]
userN = myresult[0]
pwd = myresult[1]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', active="home")


@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact")


@app.route('/about')
def about():
    return render_template('about.html', title="About", active="about")


@app.route('/statistics')
def statistics():
    x, conn = connection()
    x.execute("SELECT status FROM rpbInfo")
    y, conn = connection()
    y.execute("SELECT * FROM history ORDER BY id DESC LIMIT 2")
    statResult = x.fetchone()
    log = y.fetchall()
    stat = statResult[0]
    lastLogin = log[1][0]
    print("LOG",log[1][0])
    global status
    sta = "statistics"
    sTa = "Statistics"
    htmlR = 'statistics.html'
    return render_template(htmlR, title=sTa, active=sta, stab=stab, num=num, userN=userN, sent=sent, stat=stat, status=status,lastLogin=lastLogin)


@app.route('/guide')
def guide():
    return render_template('guide.html', title="Guide", active="guide")

global status
status='Running'
@app.route('/settings', methods=['post', 'get'])
def settings():
    global status
    logAlert = None
    run = 'disabled'
    stop = ''
    msg='run'
    if 'username' in session:
        if request.method == 'POST':
            if request.form.get("button1"):
                run = 'disabled'
                stop = ''
                msg='run'
                status='Running'
                #while True:
                   # dap.detectObject(True)

            elif request.form.get("button2"):
                run = ''
                stop = 'disabled'
                msg='stop'
                status='Idle'
                #dap.detectObject(False)
            if request.form.get("button3"):
                rebootAlert = "Are you sure you want to Reboot the RPB?"
                return render_template('mesAlert.html', rebootAlert=rebootAlert)
            elif request.form.get("button4"):
                shutdownAlert = "Are you sure you want to SHUTDOWN the RPB?"
                return render_template('mesAlert.html', shutdownAlert=shutdownAlert)
    else:
        logAlert = "Do you want to login as Admin?"
        return render_template('mesAlert.html', logAlert=logAlert)
    return render_template('settings.html', title="Settings", active="settings",logOn="logout", run=run, stop=stop, msg=msg, stab=stab, num=num, userN=userN, pwd=pwd)


@app.route('/adminlogin', methods=['post', 'get'])
def adminlogin():
    error = None
    if request.method == 'POST':
        fname = request.form.get('username')
        fpass = request.form.get('password')

        if fname != userN or fpass != pwd:
            error = 'Invalid Credentials. Please try again.'
        else:
            x, conn = connection()
            x.execute("INSERT INTO history(login) VALUES (CURRENT_TIMESTAMP)")
            conn.commit()
            session['username'] = fname
            return redirect(url_for('settings'))
    return render_template('adminlogin.html', title="AdminLogin", error=error)


@app.route('/adminlogout')
def adminlogout():
    logoutAlert = "Are you sure you want to Logout?"
    return render_template('mesAlert.html', logoutAlert=logoutAlert)


@app.route('/destroySession')
def destroySession():
    session.pop('username', None)
    session.clear()
    return render_template('index.html', title="Home", active="home")


@app.route('/alertEdit')
def alertEdit():
    editAlert = "Are you sure you want to edit the following information?"
    return render_template('mesAlert.html', editAlert=editAlert)


@app.route('/alert')
def alert():
    sureReset = "Are you sure you want to reset your username and password?"
    return render_template('mesAlert.html', sureReset=sureReset)


@app.route('/reset')
def reset():
    rname = "admin"
    rpwd = "recycle"
    c, conn = connection()
    c.execute("UPDATE user SET name = %s, password = %s WHERE id = 1", (rname, rpwd))
    conn.commit()
    resetOk = "Successfully reset the username and password."
    session.clear()
    return render_template('mesAlert.html', resetOk=resetOk)


@app.route('/editInfo', methods=['post', 'get'])
def editInfo():
    x, conn = connection()
    if request.method == 'POST':
        s = request.form.get('stablish')
        n = request.form.get('name')
        p = request.form.get('pass')
        no = request.form.get('number')
        print(s,n,p,no)
        x.execute("UPDATE rpbInfo SET stablishment = %s, phoneNo = %s WHERE id = 1", (s, no))
        x.execute("UPDATE user SET name = %s, password = %s WHERE id = 1", (n, p))
        conn.commit()
        editSure = "You updated the registered information."
        return render_template('mesAlert.html', editSure=editSure)
    return render_template('editInfo.html',stab=stab,num=num,userN=userN,pwd=pwd)


@app.route('/reboot')
def rebootBtn():
    return os.system("reboot")


@app.route('/shutdwon')
def shutdownBtn():
    return os.system("shutdown now")



if __name__ == '__main__':
    app.run(debug=True, host='192.168.8.174',port="5000")
    #app.run()