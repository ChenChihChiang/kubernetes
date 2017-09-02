#!flask/bin/python
from flask import Flask, redirect, abort, render_template, request, url_for
import os
import subprocess
import json
import pymysql

app = Flask(__name__)

@app.route('/ip')
def ip():

    os.system("curl ipinfo.io > /root/templates/ip.html")
    return render_template('ip.html')


@app.route('/hostname')
def hostname():

    os.system("hostname > /root/templates/hostname.html")
    return render_template('hostname.html')

@app.route('/login')
def login():

    result = os.popen('curl ipinfo.io')

    ip =  json.load(result)

    source = ip['ip']

    db = pymysql.connect("54.254.204.187","nuwa","nuWA88**","login_time")
    cursor = db.cursor()
    sql = """INSERT INTO login_time(ip) VALUES ('%s')""" % source
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()
  
    return redirect(url_for('time'))

@app.route('/time')
def time():
    
    db = pymysql.connect("54.254.204.187","nuwa","nuWA88**","login_time")
    cursor = db.cursor()
    sql = """select ip, DATE_FORMAT(time,'%Y-%m-%d %T') from login_time.login_time"""
    cursor.execute(sql)
    db.commit()

    data = cursor.fetchall()
    
    os.system("rm -rf /root/templates/time.html") 
    f = open('/root/templates/time.html','w')
    
    for i in data:

        f.write(str(i))
        f.write("<BR>")

    f.close()
    
    return render_template('time.html')

@app.route('/local')
def local():

    f = open('/root/templates/local.html','w')
    
    output = os.popen('ls /root/')
    
    while 1:
        line = output.readline()
        if not line: break
        f.write(line)
        f.write("<BR>")

    f.close()
    return render_template('local.html')

@app.route('/ebs')
def ebs():

    f = open('/root/templates/ebs.html','w')

    output = os.popen('ls /ebs/')

    while 1:
        line = output.readline()
        if not line: break
        f.write(line)
        f.write("<BR>")

    f.close()
    return render_template('ebs.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,threaded=True,debug=True)
