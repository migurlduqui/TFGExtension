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
DB_PATH = __file__[:-6]+"DB\\DB.sqlite"



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
    Blob = str(Blob)
    uid = data["uid"]

    cur.execute("""INSERT OR IGNORE INTO PrivacySettings (Blob,uid) VALUES (?,?)""", 
                        (Blob,uid))
    conn.commit()
    
    pass

def Cookieslog(data): #Base DataBase Logger for several loggers
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    Blob = data["blob"]
    Blob = str(Blob)
    uid = data["uid"]

    cur.execute("""INSERT OR IGNORE INTO Cookies (cookies,uid) VALUES (?,?)""", 
                        (Blob,uid))
    conn.commit()
    
    pass

def HistorialLog(data): #Base DataBase Logger for several loggers
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    Blob = data["blob"]
    Blob = str(Blob)
    uid = data["uid"]

    cur.execute("""INSERT OR IGNORE INTO Historial (historie,uid) VALUES (?,?)""", 
                        (Blob,uid))
    conn.commit()
    
    pass

def Proxielog(data): #Base DataBase Logger for several loggers
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    Blob = data["blob"]
    Blob = str(Blob)
    uid = data["uid"]

    cur.execute("""INSERT OR IGNORE INTO Proxies (proxy,uid) VALUES (?,?)""", 
                        (Blob,uid))
    conn.commit()
    
    pass

def Extensionslog(data): #Base DataBase Logger for several loggers
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    Blob = data["blob"]
    Blob = str(Blob)
    uid = data["uid"]

    cur.execute("""INSERT OR IGNORE INTO Extensions (extension,uid) VALUES (?,?)""", 
                        (Blob,uid))
    conn.commit()
    
    pass
def Downloadslog(data): #Base DataBase Logger for several loggers
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    Blob = data["blob"]
    Blob = str(Blob)
    uid = data["uid"]

    cur.execute("""INSERT OR IGNORE INTO Downloads (down,uid) VALUES (?,?)""", 
                        (Blob,uid))
    conn.commit()
    
    pass

def CPUlog(data): #Base DataBase Logger for several loggers
    
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()
    Blob = data["blob"]
    Blob = str(Blob)
    uid = data["uid"]
    cur.execute("SELECT * FROM  Cpus WHERE uid = ?", (uid,)) #https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
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
    Blob = str(Blob)
    uid = data["uid"]

    cur.execute("SELECT * FROM  OS WHERE uid = ?", (uid,)) #https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
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

    cur.execute("""INSERT OR IGNORE INTO Geolocations (latitude,longitude,uid) VALUES (?,?, ?)""", 
                        (Lat,Lon,uid))
    conn.commit()
    
    pass