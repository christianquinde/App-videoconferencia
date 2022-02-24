# -*- coding: utf-8 -*-

import sys, math, os, time, subprocess
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *  
from PyQt5.QtWidgets import *
import threading

class Ui_MainWindow(QDialog):
    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        loadUi("screen1.ui",self)
        self.Btn_ingresar.clicked.connect(self.gotoScreen2)
                

    def gotoScreen2(self):
        global nombre, server_ip, ip_me

        nombre = self.name.text()
        # leer el archivo server.conf - envia su nombre y su ip al servidor por el puerto ----
        conf_file = "server.conf"
        file = open(conf_file)
        config = file.readlines()
        server_ip = config[0]
        server_ip = server_ip[10:len(server_ip)-1]
        print(server_ip)
        #--------------------------------------------------------------------------------------
        
        # capturo la ip y guardo en un txt
        os.chdir(pwd+'/server')
        subprocess.run(['./ifconfig_ip.sh'])  #capturo la ip
        ip_me=subprocess.run(['./name_ip.py',str(nombre)],capture_output=True) # guardo nombre e ip
        ip_me=ip_me.stdout.decode()
        subprocess.run(['./borrar_mandar.sh',server_ip]) # borro archivos y mando info al servidor
        os.chdir(pwd)
        #widget.setCurrentIndex(1)
        screen2=Screen2()
        widget.addWidget(screen2)
        widget.setCurrentIndex(widget.currentIndex()+1)
        

class Screen2(QDialog):
    def __init__(self):
        super(Screen2,self).__init__()
        loadUi("screen2.ui",self)
        self.tx_label.setText(nombre)
        self.Btn_llamar.clicked.connect(self.call)
        self.Btn_llamar.setIcon(QtGui.QIcon('diseno/B5.png'))
        self.Btn_llamar.setIconSize(QtCore.QSize(40,40))
    
        os.chdir(pwd+'/server')
        subprocess.run(['sudo','rm','-R','base_datos.txt'])
        subprocess.run(['./enviar.sh',str(ip_me), server_ip])  #capturo la ip
        conts=subprocess.run(['./nombres.py'],capture_output=True)  #saco los nombres
        aaa=conts.stdout.decode()
        fila=eval(aaa) # saco los nombres en vector
        self.list_contactos.clear() # elimino los nombres al qlist
        self.list_contactos.addItems(fila) # anado los nombres al qlist
        self.list_contactos.setItemAlignment(Qt.AlignHCenter)

        os.chdir(pwd+'/receptor')
        ff=os.path.isfile('llamada_entrante.pcap')
        if ff==True:
            os.remove("llamada_entrante.pcap")
        subprocess.Popen(['python3','incoming_call.py',str(ip_me),' &'])

        self.worker = Thread_in_call()
        self.worker.start()
        self.worker.finished.connect(self.timbrar)
    
    def timbrar(self):
        global ip_name, ip_call
        os.chdir(pwd+'/receptor')
        ip_name1=subprocess.run(['python3','entrante.py',pwd],capture_output=True)  
        ip_name1=ip_name1.stdout.decode().split()     
        print(ip_name1)         
        ip_name=ip_name1[0]+" "+ip_name1[1]
        ip_call=ip_name1[2]
        os.chdir(pwd)
        self.myOtherWindow = OtherWindow()
        self.myOtherWindow.show()

    def call(self):
        global name_select, ip_dest, bitrate
        FLAG='1'
        # escogo el nombre
        os.chdir(pwd+'/server')
        name_select = self.list_contactos.currentItem().text() #selecciono el nombre
        resul1="El contacto seleccionado es: "
        resul1=resul1+name_select
        ip_dest=subprocess.run(['./ip_dest.py',str(name_select)],capture_output=True)  #saco las ips
        ip_dest=ip_dest.stdout.decode()
        
        os.chdir(pwd)
        subprocess.run(['./test_net.sh',str(ip_dest),' &'])  #hago iperf
        exi=os.path.isfile(pwd+'/server/bw/net_check.txt')
        size2=0
        while exi==False or size2<=339:
            exi=os.path.isfile(pwd+'/server/bw/net_check.txt')
            if exi==True:
                size2=os.path.getsize(pwd+'/server/bw/net_check.txt')
        '''
        bw=subprocess.run(['python3','get_bw.py',"server/bw"],capture_output=True)
        bw=bw.stdout.decode().split() 
        bw_value=float(bw[0])
        bw_units=bw[1]

        if bw_units=='kbits/sec':
            bw_value=bw_value*1000
        else:
            bw_value=bw_value*1000000
        '''
        bw_value=1000000
        if bw_value < 500000:
            bitrate=300000
        else:
            bitrate=350000

        subprocess.Popen(['bash','server-v4l2-VP8-alsasrc-PCMA.sh',str(ip_dest),str(bitrate),' &']) #servidor
        subprocess.Popen(['bash','client2-VP8-PCMA.sh',ip_dest,' &'])#cliente
        print("BITRATE="+str(bitrate))
        self.call_window = Ui_llamada(FLAG)
        self.call_window.show()
        #self.pinger = Thread_ping(FLAG) #hilo de la llamada
        #self.pinger.start()
    
class OtherWindow(QtWidgets.QMainWindow,QPushButton):
    def __init__(self):
        super(OtherWindow,self).__init__()
        loadUi('screen3.ui',self).show()
        self.name_llamada.setText(ip_name)
        os.chdir(pwd+"/receptor")
        subprocess.run(['./tono.sh','&'])  #sueno la cancion
        os.chdir(pwd)
        self.Btn_contestar.clicked.connect(self.contestar)
        self.Btn_declinar.clicked.connect(self.declinar)

    def contestar(self):
        os.chdir(pwd)
        global bitrate, FLAG
        FLAG='0'
        
        exi=os.path.isfile(pwd+'/receptor/bw/net_check.txt')
        size2=0
        while exi==False or size2<=339:
            exi=os.path.isfile(pwd+'/receptor/bw/net_check.txt')
            if exi==True:
                size2=os.path.getsize(pwd+'/receptor/bw/net_check.txt')
        '''
        bw=subprocess.run(['python3','get_bw.py',"receptor/bw"],capture_output=True)
        bw=bw.stdout.decode().split() 
        bw_value=float(bw[0])
        bw_units=bw[1]

        if bw_units=='kbits/sec':
            bw_value=bw_value*1000
        else:
            bw_value=bw_value*1000000
        '''
        bw_value=1000000
        if bw_value < 500000:
            bitrate=300000
        else:
            bitrate=350000
        subprocess.run(['sudo','killall','play'])
        print("BITRATE="+str(bitrate))
        self.close()

        self.call_window = Ui_llamada(FLAG)
        self.call_window.show()
        subprocess.Popen(['bash','server2-v4l2-VP8-alsasrc-PCMA.sh',str(ip_call),str(bitrate),' &']) #servidor
        subprocess.Popen(['bash','client-VP8-PCMA.sh',ip_call,' &'])#cliente
        
    def declinar(self):
        subprocess.run(['sudo','killall','play'])
        subprocess.run(['sudo','killall','tcpdump'])
        self.close()

        os.chdir(pwd+'/receptor')
        ff=os.path.isfile('llamada_entrante.pcap')
        if ff==True:
            os.remove("llamada_entrante.pcap")
        subprocess.Popen(['python3','incoming_call.py',str(ip_me),' &']) 

        self.worker2 = Thread_in_call()
        self.worker2.start()
        self.worker2.finished.connect(self.timbrar)

    def timbrar(self):
        global ip_name, ip_call
        os.chdir(pwd+'/receptor')
        ip_name1=subprocess.run(['python3','entrante.py',pwd],capture_output=True)  
        ip_name1=ip_name1.stdout.decode().split()     
        print(ip_name1)         
        ip_name=ip_name1[0]+" "+ip_name1[1]
        ip_call=ip_name1[2]
        os.chdir(pwd)
        self.myOtherWindow = OtherWindow()
        self.myOtherWindow.show()

class Ui_llamada(QtWidgets.QMainWindow,QPushButton):
    def __init__(self, FLAG1):
        super(Ui_llamada,self).__init__()
        global FLAG
        os.chdir(pwd)
        FLAG=FLAG1
        loadUi("screen4.ui",self).show()
        if FLAG=='1':
            self.user2.setText(name_select) #cuando llama
        else:
            self.user2.setText(ip_name) #cuando recibe llamada
        
        self.Btn_finalizar.clicked.connect(self.end_call)

    def end_call(self):
        os.chdir(pwd)
        self.close()
        print("Cerrando........")
        subprocess.run(['sudo','killall','gst-launch-1.0'])
        subprocess.run(['sudo','killall','tcpdump'])

        os.chdir(pwd+'/receptor')
        ff=os.path.isfile('llamada_entrante.pcap')
        if ff==True:
            os.remove("llamada_entrante.pcap")
            print("borrado")
        subprocess.Popen(['python3','incoming_call.py',str(ip_me),' &'])

        
        self.worker3 = Thread_in_call()
        self.worker3.start()
        self.worker3.finished.connect(self.timbrar)

    def timbrar(self):
        global ip_name, ip_call
        os.chdir(pwd+'/receptor')
        ip_name1=subprocess.run(['python3','entrante.py',pwd],capture_output=True)  
        ip_name1=ip_name1.stdout.decode().split()     
        print(ip_name1)         
        ip_name=ip_name1[0]+" "+ip_name1[1]
        ip_call=ip_name1[2]
        os.chdir(pwd)
        self.myOtherWindow = OtherWindow()
        self.myOtherWindow.show()
        
class Thread_in_call(QThread):
    #flag = QtCore.pyqtSignal(int)
    def run(self):
        os.chdir(pwd)
        size=0
        flag1=os.path.isfile(pwd+'/receptor/llamada_entrante.pcap')
        while flag1==False or size==0:
            flag1=os.path.isfile(pwd+'/receptor/llamada_entrante.pcap')
            if flag1==True:
                size=os.path.getsize(pwd+'/receptor/llamada_entrante.pcap')

#---------------------main-----------------------------------

pwd=os.getcwd()
app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
mainwindow=Ui_MainWindow()
widget.addWidget(mainwindow)
widget.setFixedWidth(528)
widget.setFixedHeight(306)
widget.setWindowTitle('Tesis - Astudillo Quinde')
widget.setWindowIcon(QIcon('diseno/v910-ning-09a.png'))
widget.show()
sys.exit(app.exec_())