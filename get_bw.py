import statistics as stats
import os, sys

direc=sys.argv[1]
#direc="server/bw"
os.chdir(direc)
arch = "net_check.txt"
file= open(arch,"r")
datos = file.readlines()

str_bw = [s for s in datos if s.__contains__("/sec")]
str_bw = str(str_bw)
final2=str_bw.split()
texto=final2[8]
texto=texto[0:len(texto)-4]

bw=float(final2[7])
print(str(bw))
print(str(texto))
#print(str(bw)+" "+final2[8])

