#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 15:49:25 2022

@author: paul
"""

arch ="base_datos.txt"
file= open(arch)
datos = file.readlines()

cont=0
nombres=[]
for i in datos:
    fila=eval(i)
    nombres.append(fila[0])
    cont=cont+1

print(str(nombres))
    