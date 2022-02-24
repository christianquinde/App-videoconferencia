import matplotlib.pyplot as plt
import sys, os, time
import statistics as stats
import numpy as np

pwd=sys.argv[1]
os.chdir(pwd+'/receptor')
arch ="llamada_entrante.pcap"
time.sleep(1)
os.system ('tshark -r'+arch +'>'+ 'result.csv')
arch_csv='result.csv'
file= open(arch_csv)
datos = file.readlines()

for i in datos:
    yy=i.split()
    ip_origen=yy[2]
    
direc = "../server"
os.chdir(direc)
arch_base='base_datos.txt'
file= open(arch_base)
datos2 = file.readlines()

for i in datos2:
    fila=eval(i)
    comp_ip=fila[1]
    if comp_ip==ip_origen:
        nombre_origen=fila[0]
        break
    else:
        nombre_origen=ip_origen
        
print(nombre_origen)
print(ip_origen)

    