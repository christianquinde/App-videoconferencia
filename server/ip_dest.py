#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 15:49:25 2022

@author: paul
"""

import matplotlib.pyplot as plt
import sys, os
import statistics as stats
import numpy as np

arch ="base_datos.txt"
file= open(arch)
datos = file.readlines()

name=sys.argv[1]
#name = "Pedro Astudillo"
cont=0
for i in datos:
    fila=eval(i)
    if str(name)==str(fila[0]):
        ip_dest=fila[1]
    cont=cont+1

print(str(ip_dest))
    