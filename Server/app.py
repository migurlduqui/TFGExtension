

#importing the necessary libraries 
from flask import Flask, request
from markupsafe import escape
import logging

#creating an instance of the Flask class 
app = Flask(__name__)




@app.route("/")
def hello_world():
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

#conda activate servers
#flask --app C:\Users\migue\Documents\TFG\TFGExtension\Server\app run
