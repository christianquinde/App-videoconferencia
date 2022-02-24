#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 21:20:41 2022

@author: paul
"""

import matplotlib.pyplot as plt
import sys, os
import statistics as stats
import numpy as np

name = sys.argv[1]

#name="Paul Astudillo"

arch ="ip.txt"
file= open(arch)
datos = file.readlines()
flag=0
for i in datos:
    encontrar=i.rfind("tun0:")
    if encontrar>=0:
        flag=1
    
    if flag==1:
        encontrar2=i.find("inet")
        if encontrar2>=0:
            final=i.find("netmask")
            ip=i[encontrar2+5:final-2]
            flag=0

file = open("name_ip.txt", "w")
file.write(str(name)+" "+str(ip))
file.close()

print(str(ip))

        
 