import socket
from sre_parse import State 
import tkinter as tk
import time
from random import *

#************************************************************************
#   h=input("ip des rechners eingeben (z.b. '192.168.178.24') : ")      *
h='192.168.2.198'                                                           #
#************************************************************************

twin = tk.Canvas(width=900, height=1100)
twin.master.title("Digitaler Zwilling")
twin.grid(row=0, column=0) 
twin.update() 


        

class Transportband():
    def __init__(self,x0,y0,x1,y1) -> None:
        twin.create_line(x0, y0, x1, y1)#bandkörper
        twin.create_line(x0, y0+20, x1, y1+20)
        twin.create_line(x0, y0, x0, y1+20)
        twin.create_line(x1, y0, x1, y1+20)
        self.__marke=twin.create_line(122,400,122,420)
        self.__touchspeicher={}
        pass

    def bewege_band(self):
        global sensorkontakt
        global hauptbandspeed
        global teile
        if hauptbandspeed !=0:                   #"bandnaht" läuft sichtbar
            twin.move(self.__marke,1,0)
        if twin.coords(self.__marke)[0] > 890:
            twin.move(self.__marke,-780,0)
        
        for i in range(1,7):
            sensorkontakt[i]=0        
        for teilnr in range(1,len(teile)+1):                  #(nr+1)):
            #####################
            if twin.coords(teile[teilnr])[2] < 900:
                
            ########################
                #für jedes teil wird an jedem stopper geprüft, ob es berührt----------------------------------
                self.__touchspeicher[teilnr]=0
                stopper=[Stopper1,Stopper2,Stopper3,Stopper4,Stopper5,Stopper6]
                for stoppnr in range(1,7):              #an jedem stopper
                    if stopperhindernis[stoppnr] <= twin.coords(teile[teilnr])[2] and stopperhindernis[stoppnr] > twin.coords(teile[teilnr])[0]:
                        self.__touchspeicher[teilnr]=1
                        twin.itemconfig(stopper[stoppnr-1].stopper, fill="red")
                        #++++++++++++zurückschieben, wenns klemmt++++++++++++++++++++++
                        while stopperhindernis[stoppnr] < twin.coords(teile[teilnr])[2]:
                            twin.move(teile[teilnr],-1,0)
                        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    if twin.coords(teile[teilnr])[2] > (stopperhindernis[stoppnr] + 5):     #wenn es durchgefahren ist
                        self.__touchspeicher[teilnr]=0
                        twin.itemconfig(stopper[stoppnr-1].stopper, fill="lightgrey")
                #-------------------------------------------------------------------------------------------
                #wenn kein stopper berührt, wird geprüft, ob es in anderes teil (vorgänger) reinfährt-----
                if self.__touchspeicher[teilnr]==0:        
                    if teilnr == 1:                     #erstes teil : 
                        twin.move(teile[teilnr],1,0)    #bewegen (keine kollision möglich)                
                    if teilnr > 1:                      #ab zweitem teil : prüfe ob kollision !
                        if twin.coords(teile[teilnr])[2] < twin.coords(teile[teilnr-1])[0]:
                            twin.move(teile[teilnr],1,0) #nur bewegen, wenn keine kollision
                        if twin.coords(teile[teilnr])[2] > twin.coords(teile[teilnr-1])[0]:
                            #++++++++++++zurückschieben, wenns überlappt++++++++++++++++++++++
                            twin.move(teile[teilnr],-1,0)
                            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #####################
            else:
                twin.move(teile[teilnr],1,0)
                twin.itemconfig(Stopper6.stopper, fill="lightgrey")       #27.5.22 Sonst bleibt Farbe immer rot
            ########################
            #------------------------------------------------------------------------------------------
            #suche sensorkontakte für jedes teil (schleife ganz oben) und jeden sensor--------
            sensor=[414,444,636,674,814,0,]                #Sensor Ort (x0+16)

            for sensornummer in range(1,6):
                if twin.coords(teile[teilnr])[2] ==sensor[sensornummer-1]:       #sensor[sensornummer]:
                    sensorkontakt[sensornummer]=1                
                    
            #---------------------------------------------------------------------------------
            #sensorfarbe ändern bei erkanntem teil
            if sensorkontakt[1]!=0:
                twin.itemconfig(Sensor1.sensor, fill="red")
            else:
                twin.itemconfig(Sensor1.sensor, fill="lightgrey")
            if sensorkontakt[2]!=0:
                twin.itemconfig(Sensor2.sensor, fill="red")
            else:
                twin.itemconfig(Sensor2.sensor, fill="lightgrey")
            if sensorkontakt[3]!=0:
                twin.itemconfig(Sensor3.sensor, fill="red")
            else:
                twin.itemconfig(Sensor3.sensor, fill="lightgrey")
            if sensorkontakt[4]!=0:
                twin.itemconfig(Sensor4.sensor, fill="red")
            else:
                twin.itemconfig(Sensor4.sensor, fill="lightgrey")
            if sensorkontakt[5]!=0:
                twin.itemconfig(Sensor5.sensor, fill="red")
            else:
                twin.itemconfig(Sensor5.sensor, fill="lightgrey")

            if sensorkontakt[1]!=0:              #automatikbetrieb der beckhoff auch ohne auftrag!!
                Stopper2.stop_zu_auto(2)
                Stopper3.stop_zu_auto(3)
                
            if sensorkontakt[4]!=0:              #selbiges bei modul3
                Stopper4.stop_zu_auto(4)
                Stopper6.stop_zu_auto(6)

    
#************************************************************************
#   Sensoren, RFID-Antennen                                             *
#************************************************************************    
class Sensor():
    def __init__(self,x0,y0,x1,y1) -> None:
        self.sensor=twin.create_rectangle(x0,y0,x1,y1,fill="lightgrey")           #Sensor
        twin.create_line(x0+6,y0+20, x1-4, y1+20, dash=(2,4))         #Sensorstrahl
        pass

class RFID():
    def __init__(self,x0,y0,x1,y1) -> None:
        self.rfid=twin.create_rectangle(x0,y0,x1,y1,fill='lightgrey')
        antenne[0]=0
        antenne[1]=0
        antenne[2]=0
        pass

    def rfid_erkennen(self,antennen_nr):
        global antenne
        rfid=[[246,260],[366,380],[766,780]]
        #for i in range(0,3):                #für alle alle rfid-antennen (0..3)
        teilx = 1                       #beginne mit teil1
        #while teilx in range(1,len(teile)): #< nr+1:             #für alle teile
        for teilx in range(1,len(teile)+1):
            #print("test antenne :",i," teil : ",teilx)
            #mitte = (twin.coords(rfid[i])[0] + twin.coords(rfid[i])[1]) / 2     #teil unter rfid-antenne ?
            mitte=(rfid[antennen_nr][0]+rfid[antennen_nr][1])/2
            if mitte > twin.coords(teile[teilx])[0] and mitte < twin.coords(teile[teilx])[2]:
                if antennen_nr==0:
                    twin.itemconfig(RFID1.rfid , fill="red")                            #teil erkannt : rfid-antenne rot
                if antennen_nr==1:
                    twin.itemconfig(RFID2.rfid , fill="red")
                if antennen_nr==2:
                    twin.itemconfig(RFID3.rfid , fill="red")
                antenne[antennen_nr] = teilx      #in antenne(antennennummer) steht die nummer des erkannten produkts
                #print("antenne : ",i," teil erkannt :",teilx)
                #teilx = nr+1            #teil erkannt : nicht weitersuchen in der teileliste
                break
            else:
                teilx += 1       #kein teil erkannt : nächstes
                if antennen_nr==0:
                    twin.itemconfig(RFID1.rfid , fill="lightgrey")                            #teil erkannt : rfid-antenne rot
                if antennen_nr==1:
                    twin.itemconfig(RFID2.rfid , fill="lightgrey")
                if antennen_nr==2:
                    twin.itemconfig(RFID3.rfid , fill="lightgrey")
                antenne[antennen_nr] = 0          #in antenne(antennennummer) steht 0, wenn kein produkt erkannt !

#************************************************************************
#   Anzeigen und Aktoren                                                *
#************************************************************************

class Anzeige():
    def __init__(self,x0,y0,x1,y1,Modul) -> None:
        self.start=twin.create_oval(x0,y0,x1,y1,fill="lightgrey")        #Lampe Start
        twin.create_text(x0+59,y0+8,fill="black",font="Times 10",text="Start Modul "+Modul)
        self.ack=twin.create_oval(x0,y0+20,x1,y1+20,fill="lightgrey")        #Lampe ack
        twin.create_text(x0+35,y0+28,fill="black",font="Times 10",text="Ack")
        self.busy=twin.create_oval(x0,y0+40,x1,y1+40,fill="lightgrey")        #Lampe busy
        twin.create_text(x0+37,y0+48,fill="black",font="Times 10",text="Busy")
        pass

class Stopper():
    def __init__(self,x0,y0,x1,y1,Nummer) -> None:
        self.stopper=twin.create_rectangle(x0,y0,x1,y1,fill = 'grey')                #stopper
        self.__kolben=twin.create_rectangle(x0+4,y0,x1-2,y1,fill = 'grey')            #Kolben
        self.__stopcount=0
        stopperhindernis[Nummer]=1000

        pass

    def stop_auf(self,Nummer):                          #öffne stopper wenn er zu ist
        global stopperhindernis
        #global donestop
        if stopperhindernis[Nummer] < 1000:
            if self.__stopcount < 20:
                self.__stopcount+=1
                twin.move(self.__kolben,0,-1)
            else:
                #donestop[snr]=1
                stopperhindernis[Nummer]=1000
                self.__stopcount=0
                return 1
        else:
            #donestop[snr]=1
            self.__stopcount=0
            return 0
        twin.update()
        
    def stop_zu(self,Nummer):                      # schließe den stopper mit der nummer snr, mit busy-erkennung
        #global stopcount
        #global donestop
        global stopperhindernis
        if stopperhindernis[Nummer] == 1000:                     # wenn er offen ist (=10000)
            if self.__stopcount < 20 :                     # und noch nicht zu
                self.__stopcount+=1
                twin.move(self.__kolben,0,1)          # langsam zufahren ..
            else:                                   # wenn er zu ist (ende erreicht)
                if Nummer==1:
                    stopperhindernis[Nummer]=264                #koordinate des hindernisses schreiben
                if Nummer==2:
                    stopperhindernis[Nummer]=384
                if Nummer==3:
                    stopperhindernis[Nummer]=414
                if Nummer==4:
                    stopperhindernis[Nummer]=647 #+5
                if Nummer==5:
                    stopperhindernis[Nummer]=784
                if Nummer==6:
                    stopperhindernis[Nummer]=814
                self.__stopcount=0
                #donestop[snr]=1
                return 1
        else:
            self.__stopcount=0
            #donestop[snr]=1
            return 1       
        twin.update()

    def stop_zu_auto(self,Nummer):                 # schließe den stopper mit der nummer snr. ohne busy
        global stopperhindernis
        if stopperhindernis[Nummer] == 1000:            # wenn er offen ist (=10000)
            #twin.move(self.__kolben[Nummer],0,20)    #die zahlenwerte werden dann bei der kollisionserkennung benutzt
            if Nummer==1:
                stopperhindernis[Nummer]=264
                twin.move(Stopper1.__kolben,0,20)
            if Nummer==2:
                stopperhindernis[Nummer]=384
                twin.move(Stopper2.__kolben,0,20)
            if Nummer==3:
                stopperhindernis[Nummer]=414
                twin.move(Stopper3.__kolben,0,20)
            if Nummer==4:
                stopperhindernis[Nummer]=644
                twin.move(Stopper4.__kolben,0,20)
            if Nummer==5:
                stopperhindernis[Nummer]=784
                twin.move(Stopper5.__kolben,0,20)
            if Nummer==6:
                stopperhindernis[Nummer]=814
                twin.move(Stopper6.__kolben,0,20)
        twin.update()

    def stop_auf_auto(self,Nummer):                      #öffne stopper wenn er zu ist
        if stopperhindernis[Nummer] < 1000:
            stopperhindernis[Nummer]=1000
            if Nummer==1:
                twin.move(Stopper1.__kolben,0,-20)
            if Nummer==2:
                twin.move(Stopper2.__kolben,0,-20)
            if Nummer==3:
                twin.move(Stopper3.__kolben,0,-20)
            if Nummer==4:
                twin.move(Stopper4.__kolben,0,-20)
            if Nummer==5:
                twin.move(Stopper5.__kolben,0,-20)
            if Nummer==6:
                twin.move(Stopper6.__kolben,0,-20)
        twin.update()
    

    

#************************************************************************
#   Variablen                                                           *
#************************************************************************
teil1a, teil1b,teil2, teil3a, teil3b ={},{},[],[],[]        #Initalisieren der Lager
kanbana, kanbanb=1,1           #Variablen Kanban Modul1
                        

teile={}        #Liste der Teile auf dem Hauptförderband
uid={}          #uid der RFID-Tags
antenne={}
antenne[0]=0
antenne[1]=0
antenne[2]=0
antenne[3]=0
antenne[4]=0
rfid_tag={}     #Nutzdaten RFID
rfid_tag[0]=0
rfid_tag[1]=0
rfid_tag[2]=0
rfid_tag[3]=0
busy1,busy2,busy3a, busy3b=0,0,0,0
start1,start2,start3a,start3b=0,0,0,0
order1,order2,order3a,order3b=0,0,0,0
ack1,ack2,ack3a,ack3b=0,0,0,0
ready1, ready2, ready3a, ready3b=1,1,1,1
done2, done3a, done3b=0,0,0                        #Interne Weiterschaltbedingung

stopperhindernis=[1,2,3,4,5,6,7]
sensorkontakt=[1,2,3,4,5,6,7]
hauptbandspeed=0


#************************************************************************
#   Module                                                              *
#************************************************************************

class Modul1():
    def __init__(self) -> None:
        
        twin.create_line(10, 270, 280, 270)#rahmen modul1
        twin.create_line(10, 550, 280, 550)
        twin.create_line(280,270, 280, 400)
        twin.create_line(280,420, 280, 550)
        twin.create_line(10,270, 10, 550)

        twin.create_rectangle(118,400,142,320)  #drehpaletten
        p1=twin.create_rectangle(120,400,140,320)
        p2=twin.create_rectangle(120,420,140,500)
        twin.create_rectangle(118,420,142,500)

        twin.create_rectangle(118,292,142,315) #stapellager
        twin.create_rectangle(120,295,140,315)
        twin.create_rectangle(118,525,142,505) 
        twin.create_rectangle(120,527,140,505)
    
        teil1a[1]=twin.create_oval(120,400,140,380,fill="blue")     #Teile generieren
        teil1a[2]=twin.create_oval(120,380,140,360,fill="blue")
        teil1a[3]=twin.create_oval(120,360,140,340,fill="blue")
        teil1a[4]=twin.create_oval(120,340,140,320,fill="blue")
        teil1a[5]=twin.create_oval(120,295,140,315,fill="blue")
        teil1b[1]=twin.create_oval(120,420,140,440,fill="red")
        teil1b[2]=twin.create_oval(120,440,140,460,fill="red")
        teil1b[3]=twin.create_oval(120,460,140,480,fill="red")
        teil1b[4]=twin.create_oval(120,480,140,500,fill="red")
        teil1b[5]=twin.create_oval(120,505,140,525,fill="red")

        self.__teilerk1, self.__teilerk2=0,0                 #Modul1 Geschwindigkeit Kanban default=1
        self.__k1a, self.__k1b=0,0
        self.__i1, self.__i2=0,0
        self.__nr=0
        self.__State=0
        pass

    def kanban_teila(self):
          #wenn kanbana > 4, läuft kanban !  
        global kanbana      
        self.__teilerk1+=1
        if self.__teilerk1 > 8:
            self.__teilerk1=1
            if self.__k1a==0:    
                teil1a[1]=twin.create_oval(120,295,140,315,fill="blue")     ##Teile generieren schublager
                teil1a[2]=twin.create_oval(120,295,140,315,fill="blue") 
                teil1a[3]=twin.create_oval(120,295,140,315,fill="blue")
                teil1a[4]=twin.create_oval(120,295,140,315,fill="blue")
                
            if self.__k1a <21:
                twin.move(teil1a[1],0,1)
                self.__k1a+=1
            if self.__k1a > 20 and self.__k1a <41:
                twin.move(teil1a[1],0,1)
                twin.move(teil1a[2],0,1)
                self.__k1a+=1   
            if self.__k1a > 40 and self.__k1a <61:
                twin.move(teil1a[1],0,1)
                twin.move(teil1a[2],0,1)
                twin.move(teil1a[3],0,1)
                self.__k1a+=1
            if self.__k1a > 60 and self.__k1a <84:
                twin.move(teil1a[1],0,1)
                twin.move(teil1a[2],0,1)
                twin.move(teil1a[3],0,1)
                twin.move(teil1a[4],0,1)
                self.__k1a+=1
            if self.__k1a == 84:
                self.__k1a=0
                kanbana=1
                #twin.itemconfig(p1, fill="GhostWhite")
                self.__teilerk1=1

    def kanban_teilb(self):
        #wenn kanbanb> 4, läuft kanbanb !
        #twin.itemconfig(p2, fill="lightgrey")
        global kanbanb      
        self.__teilerk2+=1
        if self.__teilerk2 > 8:
            self.__teilerk2=1
            if self.__k1b==0: 
                teil1b[1]=twin.create_oval(120,505,140,525,fill="red")  ##Teile generieren schublager
                teil1b[2]=twin.create_oval(120,505,140,525,fill="red")
                teil1b[3]=twin.create_oval(120,505,140,525,fill="red")
                teil1b[4]=twin.create_oval(120,505,140,525,fill="red")
            if self.__k1b <21:
                twin.move(teil1b[1],0,-1)
                self.__k1b+=1
            if self.__k1b > 20 and self.__k1b <41:
                twin.move(teil1b[1],0,-1)
                twin.move(teil1b[2],0,-1)
                self.__k1b+=1    
            if self.__k1b > 40 and self.__k1b <61:
                twin.move(teil1b[1],0,-1)
                twin.move(teil1b[2],0,-1)
                twin.move(teil1b[3],0,-1)
                self.__k1b+=1
            if self.__k1b > 60 and self.__k1b <84:
                twin.move(teil1b[1],0,-1)
                twin.move(teil1b[2],0,-1)
                twin.move(teil1b[3],0,-1)
                twin.move(teil1b[4],0,-1)
                self.__k1b+=1
            if self.__k1b == 84:
                self.__k1b=0
                kanbanb=1
                #win.itemconfig(p2, fill="GhostWhite") 
            
    def erzeuge_teil1a(self):    
        global kanbana     
        global busy1   
        if kanbana < 5:
            if self.__i1 < 20:
                self.__i1+=1
                for xyz in range (kanbana,5):
                    twin.move(teil1a[xyz],0,1)
                    
            if self.__i1 == 20:
                #kanbana=kanbana+1
                self.__nr+=1 
                teile[self.__nr] = twin.create_oval(120,400,140,420,fill="blue")
                twin.delete(teil1a[kanbana])
                #-------------------uid erzeugen und schreiben-----
                doppel=1
                uid[self.__nr] = randint(1,255)                #generiere zufalls-uid
                while doppel == 1:                      #solange diese schon vorhanden
                    doppel = 0
                    for teilnr in range(1,self.__nr):          #für alle teile bis nr aktuelles teil)
                        if uid[teilnr] == uid[self.__nr]:      #falls schon vorhanden
                            doppel = 1                  #melden
                            uid[self.__nr] = randint(1,255)    #neue generieren
                #--------------------------------------------------
                kanbana+=1
                busy1=0
                self.__i1=0

    def erzeuge_teil1b(self):      
        global kanbanb
        global busy1
        if kanbanb < 5:
            if self.__i2 < 20:
                self.__i2+=1
                for xyz in range (kanbanb,5):
                    twin.move(teil1b[xyz],0,-1)
            if self.__i2 == 20:
                self.__nr+=1
                teile[self.__nr] = twin.create_oval(120,400,140,420,fill="red")
                #teile.append(teil1b[kanbanb])
                twin.delete(teil1b[kanbanb])
                #teil1b.remove(teil1b[kanbana])
                #-------------------uid erzeugen und schreiben-----
                doppel=1
                uid[self.__nr] = randint(1,255)                #generiere zufalls-uid
                while doppel == 1:                      #solange diese schon vorhanden
                    doppel = 0
                    for teilnr in range(1,self.__nr):          #für alle teile bis nr aktuelles teil)
                        if uid[teilnr] == uid[self.__nr]:      #falls schon vorhanden
                            doppel = 1                  #melden
                            uid[self.__nr] = randint(1,255)    #neue generieren
                #--------------------------------------------------
                kanbanb+=1
                busy1=0
                self.__i2=0

    def Bewegungsablauf(self):
    #-------------------------------------------------------------------------|
    #   SPS Modul 1                                                           |  
    #-------------------------------------------------------------------------|
        global kanbana
        global kanbanb
        global start1
        global ack1
        global order1
        global busy1
        global done
        if kanbana > 4:
            module1.kanban_teila()   #kanban_teila()
        if kanbanb > 4:
            module1.kanban_teilb()   #kanban_teilb()
        if start1==1:
            ack1=1
            if order1 > 0:
                busy1=1
        if start1==0 and ack1==1:
            ack1=0
        if order1==1 and busy1==1:
            module1.erzeuge_teil1a()        #erzeuge_teil1a()        
        if order1==2 and busy1==1:
            module1.erzeuge_teil1b()           #erzeuge_teil1b()
        if order1==3 and busy1==1:
            Stopper1.stop_auf_auto(1)       #stop_auf_auto(1)
            busy1=0
        if order1==4 and busy1==1:
            Stopper1.stop_zu_auto(1)        #stop_zu_auto(1)
            busy1=0
        if order1==10 and busy1==1:
            if self.__State ==0:
                done=Stopper1.stop_zu(1)
                if done==1:
                    self.__State=1
            if self.__State ==1:
                done=Stopper1.stop_auf(1)
                if done==1:
                    self.__State=2 
            if self.__State ==2:
                done=Stopper1.stop_zu(1)
                if done==1:
                    self.__State=3
            if self.__State ==3:
                done=Stopper1.stop_auf(1)
                if done==1:
                    self.__State=4
            if self.__State ==4:
                done=Stopper1.stop_zu(1)         #stop_zu(1)
                if done==1:
                    self.__State=5
            if self.__State ==5:
                done=Stopper1.stop_auf(1)        #stop_auf(1)
                if done==1:
                    self.__State=6
            if self.__State ==6:
                busy1=0
                self.__State=0    
        
        


class Modul2():
    def __init__(self) -> None:
        twin.create_line(290, 270, 570, 270)    #rahmen modul2
        twin.create_line(290, 550, 570, 550)
        twin.create_line(570,270, 570, 400)
        twin.create_line(570,420, 570, 550)
        twin.create_line(290,270, 290, 400)
        twin.create_line(290,420, 290, 550)

        twin.create_rectangle(364,430,393,450)  #Notlager
        twin.create_rectangle(362,428,393,452)
        twin.create_rectangle(416,420,425,500)  # ??

        twin.create_oval(364,430,384,450,fill="black")  #Teil generieren teila
        twin.create_oval(394,470,414,490,fill="red")    #Teil generieren teilb

        self.__temp_neuteil=0
        self.__j=0
        self.__nr2=0
        self.__State2=0
        self._Schrankensteuerzng=1
        self.__done2=0
        pass

    def erzeuge_teil2a(self):
        if self.__j==0:
            self.__temp_neuteil = twin.create_oval(364,430,384,450,fill="black")
        if self.__j < 30:
            self.__j+= 1
            twin.move(self.__temp_neuteil,1,0)        
        if self.__j>= 30 and self.__j<60:
            self.__j+= 1
            twin.move(self.__temp_neuteil,0,-1)  
        if self.__j==60:
            self.__nr2+=1                   #nummer des aktuellen bauteils
            twin.delete(self.__temp_neuteil) 
            twin.itemconfig(teile[self.__nr2], fill="black") #aktuelles bauteil bearbeiten
            self.__j=0
            self.__done2=1

    def erzeuge_teil2b(self):
        if self.__j==0:
            self.__temp_neuteil = twin.create_oval(394,470,414,490,fill="red")
        if self.__j < 70: 
            self.__j+= 1
            twin.move(self.__temp_neuteil,0,-1)
        if self.__j==70:
            self.__nr2+=1                   #nummer des aktuellen bauteils
            twin.delete(self.__temp_neuteil) 
            twin.itemconfig(teile[self.__nr2], fill="red") #aktuelles bauteil bearbeiten
            self.__j=0
            self.__done2=1

    def Bewegungsablauf(self):
    #-------------------------------------------------------------------------|
    #   SPS Modul 2                                                           |  
    #-------------------------------------------------------------------------|
        global start2
        global ack2
        global order2
        global busy2
        if start2==1:                           #ab hier handshake : start -> acknowledge
            ack2=1
            if order2 > 0:                      #kein nullauftrag : -> busy
                busy2=1
                self.__Schrankensteuerung=1                #Anpassung damit RFID-Schranke automatisch öffnet 29.03.22
        if start2==0 and ack2==1:               #MES hat erkannt -> start=0 -> ack=0
            Stopper3.stop_zu_auto(3)
            ack2=0
            
        if order2==1 and busy2==1:
            if self.__Schrankensteuerung==1:
                Stopper2.stop_auf_auto(2)
                self.__Schrankensteuerung=0
            if sensorkontakt[1]!=0:              #aktion erst, wenn teil im bestückungsbereich
                module2.erzeuge_teil2b()
                if self.__done2==1:
                    Stopper3.stop_auf_auto(3)
                    Stopper2.stop_zu_auto(2)
            if sensorkontakt[2]!=0:              #fertig, wenn bereich verlassen
                Stopper3.stop_zu_auto(3)
                #stop_auf_auto(2)       # 19.3. : sonst läuft normalbetrieb nicht !!!
                self.__done2=0
                busy2=0
        if order2==2 and busy2==1:
            if self.__Schrankensteuerung==1:
                Stopper2.stop_auf_auto(2)
                self.__Schrankensteuerung=0
            if sensorkontakt[1]!=0:              #aktion erst, wenn teil im bestückungsbereich
                module2.erzeuge_teil2a()
                if self.__done2==1:
                    Stopper3.stop_auf_auto(3)
                    Stopper2.stop_zu_auto(2)
            if sensorkontakt[2]!=0:              #fertig, wenn bereich verlassen
                Stopper3.stop_zu_auto(3)
                #stop_auf_auto(2)       # 19.3. : sonst läuft normalbetrieb nicht !!!
                self.__done2=0
                busy2=0 
        if order2==3 and busy2==1:
    ##            donestop[2]=0
    ##            stop_auf(2)
    ##            if donestop[2]==1:
    ##                busy2=0
            Stopper2.stop_auf_auto(2)
            busy2=0
        if order2==4 and busy2==1:
    ##            donestop[2]=0
    ##            stop_zu(2)
    ##            if donestop[2]==1:
    ##                busy2=0
            Stopper2.stop_zu_auto(2)
            busy2=0
        if order2==5 and busy2==1:
    ##            donestop[3]=0
    ##            stop_auf(3)
    ##            if donestop[3]==1:
    ##                busy2=0
            #print("tor auf")
            Stopper3.stop_auf_auto(3)
            busy2=0
        if order2==6 and busy2==1:
    ##            donestop[3]=0
    ##            stop_zu(3) 
    ##            if donestop[3]==1:
    ##                busy2=0
            Stopper3.stop_zu_auto(3)
            busy2=0
        if order2==10 and busy2==1:
            if self.__State2 ==0:
                done2=Stopper2.stop_zu(2)
                if done2==1:
                    self.__State2=1
            if self.__State2 ==1:
                done2=Stopper2.stop_auf(2)
                if done2==1:
                    self.__State2=2 
            if self.__State2 ==2:
                done2=Stopper2.stop_zu(2)
                if done2==1:
                    self.__State2=3
            if self.__State2 ==3:
                done2=Stopper2.stop_auf(2)
                if done2==1:
                    self.__State2=4
            if self.__State2 ==4:
                done2=Stopper2.stop_zu(2)         #stop_zu(1)
                if done2==1:
                    self.__State2=5
            if self.__State2 ==5:
                done2=Stopper2.stop_auf(2)        #stop_auf(1)
                if done2==1:
                    self.__State2=6
            if self.__State2 ==6:
                busy2=0
                self.__State2=0 
    
class Modul3a():
    def __init__(self) -> None:
        twin.create_line(580, 130, 860, 130)    # Rahmen Modul 3a
        twin.create_line(580, 130, 580, 400)
        twin.create_line(860, 130, 860, 400)
        

        twin.create_rectangle(693,335,715,305)  #schachtlager 3a
        twin.create_rectangle(691,335,717,305)
        twin.create_rectangle(663,335,685,305)
        twin.create_rectangle(661,335,687,305)
        twin.create_rectangle(633,335,655,305)
        twin.create_rectangle(631,335,657,305)

        twin.create_rectangle(620,335,820,355)  #Schublager 3a
        twin.create_rectangle(618,333,820,353)

        twin.create_oval(694,305,714,325,fill="red")    #teile im lager von Modul 3a
        twin.create_oval(664,305,684,325,fill="blue")
        twin.create_oval(634,305,654,325,fill="black")
        self.__kb=0
        self.__temp_neuteil3a=0
        self.__nr3=0
        self.__State=0
        pass
        
    def erzeuge_teil3aa(self):
        global done3a
        global busy3a
        if self.__kb==0:
            self.__temp_neuteil3a= twin.create_oval(694,305,714,325,fill="red")
        if self.__kb < 30:
            self.__kb+= 1
            twin.move(self.__temp_neuteil3a,0,1)
        if self.__kb >= 30 and self.__kb < 130:
            self.__kb+= 1
            twin.move(self.__temp_neuteil3a,1,0)
        if self.__kb >= 130 and self.__kb < 195: #+10
            if sensorkontakt[5]!=0:
                self.__kb+= 1
                twin.move(self.__temp_neuteil3a,0,1)
        if self.__kb >= 195:        
            self.__nr3+=1
            twin.delete(self.__temp_neuteil3a) 
            twin.itemconfig(teile[self.__nr3], fill="red") #aktuelles bauteil bearbeiten
            self.__kb=0
            busy3a=0
            done3a=1

    def erzeuge_teil3ab(self):
        global done3a
        global busy3a
        if self.__kb==0:
            self.__temp_neuteil3a = twin.create_oval(664,305,684,325,fill="blue")
        if self.__kb < 30:
            self.__kb += 1
            twin.move(self.__temp_neuteil3a,0,1)
        if self.__kb >= 30 and self.__kb < 160:
            self.__kb += 1
            twin.move(self.__temp_neuteil3a,1,0)
        if self.__kb >= 160 and self.__kb < 225: #+10
            if sensorkontakt[5]!=0:
                self.__kb += 1
                twin.move(self.__temp_neuteil3a,0,1)
        if self.__kb >= 225:        
            self.__nr3+=1
            twin.delete(self.__temp_neuteil3a) 
            twin.itemconfig(teile[self.__nr3], fill="blue") #aktuelles bauteil bearbeiten
            self.__kb=0
            busy3a=0
            done3a=1
            
    def erzeuge_teil3ac(self):
        global done3a
        global busy3a  
        if self.__kb==0:
            self.__temp_neuteil3a = twin.create_oval(634,305,654,325,fill="black")
        if self.__kb < 30:
            self.__kb+= 1
            twin.move(self.__temp_neuteil3a,0,1)
        if self.__kb >= 30 and self.__kb < 190:
            self.__kb += 1
            twin.move(self.__temp_neuteil3a,1,0)
        if self.__kb >= 190 and self.__kb < 255: #+10
            if sensorkontakt[5]!=0:
                self.__kb += 1
                twin.move(self.__temp_neuteil3a,0,1)
        if self.__kb >= 255:        
            self.__nr3+=1
            twin.delete(self.__temp_neuteil3a) 
            twin.itemconfig(teile[self.__nr3], fill="black") #aktuelles bauteil bearbeiten
            self.__kb=0
            busy3a=0
            done3a=1

    def Bewegungsablauf(self):
    #-------------------------------------------------------------------------|
    #   SPS Modul 3a (Teil a : oben)                                          |  
    #-------------------------------------------------------------------------|
        global ack3a
        global order3a
        global busy3a
        global done3a
        global start3a
        if start3a==1:                        #ab hier handshake-steuerung
            ack3a=1
            if order3a > 0:
                busy3a=1
        if start3a==0 and ack3a==1:
            ack3a=0
        if order3a==1 and busy3a==1:          #ab hier auswertung der order
            module3a.erzeuge_teil3aa()
            if done3a==1:
                Stopper4.stop_auf_auto(4)       # 19.3. : sonst läuft normalbetrieb nicht !!! wieder drinnen (STRR)
                Stopper6.stop_auf_auto(6)       # 19.3. : sonst läuft normalbetrieb nicht !!! wieder drinnen (STRR)
                done3a=0
                busy3a=0
        if order3a==2 and busy3a==1:
            module3a.erzeuge_teil3ab()
            if done3a==1:
                Stopper4.stop_auf_auto(4)       # 19.3. : sonst läuft normalbetrieb nicht !!! wieder drinnen (STRR)
                Stopper6.stop_auf_auto(6) 
                done3a=0
                busy3a=0
        if order3a==3 and busy3a==1:
            module3a.erzeuge_teil3ac()
            if done3a==1:
                Stopper4.stop_auf_auto(4)       # 19.3. : sonst läuft normalbetrieb nicht !!! wieder drinnen (STRR)
                Stopper6.stop_auf_auto(6) 
                done3a=0
                busy3a=0
        if order3a==4 and busy3a==1:
            #donestop[5]=0
            Stopper5.stop_auf_auto(5)
            #if donestop[5]==1:
            busy3a=0
        if order3a==5 and busy3a==1:
            #donestop[5]=0
            Stopper5.stop_zu_auto(5)
            #if donestop[5]==1:
            busy3a=0
        if order3a==6 and busy3a==1:
            #donestop[6]=0
            Stopper6.stop_auf_auto(6)
            #if donestop[6]==1:
            busy3a=0
        if order3a==7 and busy3==1:
            #donestop[6]=0
            Stopper6.stop_zu_auto(6)
            #if donestop[6]==1:
            busy3a=0
        if order3a==8 and busy3a==1:
            #donestop[4]=0
            Stopper4.stop_auf_auto(4)
            #if donestop[4]==1:
            busy3a=0  
        if order3a==9 and busy3a==1:
            #donestop[4]=0
            Stopper4.stop_zu_auto(4)
            #if donestop[4]==1:
            busy3a=0              
        if order3a==10 and busy3a==1:
            if self.__State ==0:
                done=Stopper4.stop_zu(4)
                if done==1:
                    self.__State=1
            if self.__State ==1:
                done=Stopper4.stop_auf(4)
                if done==1:
                    self.__State=2 
            if self.__State ==2:
                done=Stopper4.stop_zu(4)
                if done==1:
                    self.__State=3
            if self.__State ==3:
                done=Stopper4.stop_auf(4)
                if done==1:
                    self.__State=4 
            if self.__State ==4:
                busy3a=0
                self.__State=0         
            
        if order3a==12 and busy3a==1:
            if sensorkontakt[4]!=0:
                #bestuecke_teil3a()
                module3a.erzeuge_teil3a()
                if done3==1:
                    Stopper6.stop_auf_auto(6)
                    Stopper4.stop_auf_auto(4)
                    done3=0
                    busy3=0        

class Modul3b():
    def __init__(self) -> None:
        twin.create_line(580, 420, 580, 690)    # Rahmen Modul 3b
        twin.create_line(580, 690, 860, 690)
        twin.create_line(860, 420, 860, 690)

        twin.create_rectangle(693,470,715,500) #schachtlager 3b
        twin.create_rectangle(691,470,717,500)
        twin.create_rectangle(663,470,685,500)
        twin.create_rectangle(661,470,687,500)
        twin.create_rectangle(633,470,655,500)
        twin.create_rectangle(631,470,657,500)

        twin.create_rectangle(620,450,820,470) #Schubrutsche 3b
        twin.create_rectangle(618,448,820,472)

        twin.create_oval(694,480,714,500,fill="red")            #teile 3a
        twin.create_oval(664,480,684,500,fill="blue")
        twin.create_oval(634,480,654,500,fill="black")
        self.__k=0
        self.__nr3=0
        self.__temp_neuteil3b=0
        pass

    def erzeuge_teil3ba(self):
        global done3b
        global busy3b
        if self.__k==0:
            self.__temp_neuteil3b = twin.create_oval(694,480,714,500,fill="red")
        if self.__k < 30:
            self.__k += 1
            twin.move(self.__temp_neuteil3b,0,-1)
        if self.__k >= 30 and self.__k < 130:
            self.__k+= 1
            twin.move(self.__temp_neuteil3b,1,0)
        if self.__k >= 130 and self.__k < 180:
            if sensorkontakt[5]!=0:
                self.__k += 1
                twin.move(self.__temp_neuteil3b,0,-1)
        if self.__k >= 180:
            self.__nr3+=1
            twin.delete(self.__temp_neuteil3b) 
            twin.itemconfig(teile[self.__nr3], fill="red") #aktuelles bauteil bearbeiten
            self.__k=0
            busy3b=0
            done3b=1
        
    def erzeuge_teil3bb(self):
        global done3b
        global busy3b
        if self.__k==0:
            self.__temp_neuteil3b = twin.create_oval(664,480,684,500,fill="blue")
        if self.__k < 30:
            self.__k+= 1
            twin.move(self.__temp_neuteil3b,0,-1)
        if self.__k >= 30 and self.__k < 160:
            self.__k+= 1
            twin.move(self.__temp_neuteil3b,1,0)
        if self.__k >= 160 and self.__k < 210:
            if sensorkontakt[5]!=0:
                self.__k+= 1
                twin.move(self.__temp_neuteil3b,0,-1)
        if self.__k >= 210:
            self.__nr3+=1
            twin.delete(self.__temp_neuteil3b) 
            twin.itemconfig(teile[self.__nr3], fill="blue") #aktuelles bauteil bearbeiten
            self.__k=0
            busy3b=0
            done3b=1
            
    def erzeuge_teil3bc(self):
        global done3b
        global busy3b
        if self.__k==0:
            self.__temp_neuteil3b = twin.create_oval(634,480,654,500,fill="black")
        if self.__k < 30:
            self.__k+= 1
            twin.move(self.__temp_neuteil3b,0,-1)
        if self.__k >= 30 and self.__k < 190:
            self.__k+= 1
            twin.move(self.__temp_neuteil3b,1,0)
        if self.__k >= 190 and self.__k < 240:
            if sensorkontakt[5]!=0:
                self.__k+= 1
                twin.move(self.__temp_neuteil3b,0,-1)
        if self.__k >= 240:
            self.__nr3+=1
            twin.delete(self.__temp_neuteil3b) 
            twin.itemconfig(teile[self.__nr3], fill="black") #aktuelles bauteil bearbeiten
            self.__k=0
            busy3b=0
            done3b=1

    def Bewegungsablauf(self):
#-------------------------------------------------------------------------|
#   SPS Modul 3b (unten)                                                  |  
#-------------------------------------------------------------------------|
        global start3b
        global ack3b
        global order3b
        global busy3b
        global done3b
        if start3b==1:
            ack3b=1
            if order3b > 0:
                busy3b=1
        if start3b==0 and ack3b==1:
            ack3b=0
        if order3b==1 and busy3b==1:
            module3b.erzeuge_teil3ba()
            if done3b==1:
                Stopper6.stop_auf_auto(6)
                Stopper4.stop_auf_auto(4)
                done3b=0
                busy3b=0
        if order3b==2 and busy3b==1:
            module3b.erzeuge_teil3bb()
            if done3b==1:
                Stopper6.stop_auf_auto(6)
                Stopper4.stop_auf_auto(4)
                done3b=0
                busy3b=0
        if order3b==3 and busy3b==1:
            module3b.erzeuge_teil3bc()
            if done3b==1:
                Stopper6.stop_auf_auto(6)
                Stopper4.stop_auf_auto(4)
                done3b=0
                busy3b=0
        if order3b==12 and busy3b==1:
            if sensorkontakt[4]!=0:
                #bestuecke_teil3ba()
                module3b.erzeuge_teil3ba()
                if done3b==1:
                    Stopper6.stop_auf_auto(6)
                    Stopper4.stop_auf_auto(4)
                    done3b=0
                    busy3b=0 

class Kommunikation():
    def __init__(self) -> None:
        self.resp=0
        self.reg=0
        self.write_rfid=0
        self.read_rfid=0
        self.read_uid=0
        self.antennen_nr=0
        pass
        
    def Sendedaten_vorbereiten(self):
#-------------------------------------------------------------------------|
#   Sendedaten vorbereiten                                                |  
#-------------------------------------------------------------------------|
        global ready1, ready2, ready3a,ready3b
        global busy1,busy2,busy3a,busy3b
        global ack1, ack2, ack3a, ack3b
          
        if ready1==1:
            self.resp=self.resp | 2**0
        else:
            self.resp=self.resp & ((2**32-1) - 2**0)
        if ready2==1:
            self.resp=self.resp | 2**3
        else:
            self.resp=self.resp & ((2**32-1) - 2**3)
        if ready3a==1:
            self.resp=self.resp | 2**6
        else:
            self.resp=self.resp & ((2**32-1) - 2**6)
        if ready3b==1:
            self.resp=self.resp | 2**13
        else:
            self.resp=self.resp & ((2**32-1) - 2**13)
        if busy1==1:
            self.resp=self.resp | 2**2
        else:
            self.resp=self.resp & ((2**32-1) - 2**2)
        if busy2==1:
            self.resp=self.resp | 2**5
        else:
            self.resp=self.resp & ((2**32-1) - 2**5)
        if busy3a==1:
            self.resp=self.resp | 2**8
        else:
            self.resp=self.resp & ((2**32-1) - 2**8)
        if busy3b==1:
            self.resp=self.resp | 2**14
        else:
            self.resp=self.resp & ((2**32-1) - 2**14)
        if ack1==1:
            self.resp=self.resp | 2**1
        else:
            self.resp=self.resp & ((2**32-1) - 2**1)
        if ack2==1:
            self.resp=self.resp | 2**4
        else:
            self.resp=self.resp & ((2**32-1) - 2**4)
        if ack3a==1:
            self.resp=self.resp | 2**7
        else:
            self.resp=self.resp & ((2**32-1) - 2**7)
        if ack3b==1:
            self.resp=self.resp | 2**15
        else:
            self.resp=self.resp & ((2**32-1) - 2**15)

        

    def Senden(self):
#-------------------------------------------------------------------------|
#   Senden                                                                |  
#-------------------------------------------------------------------------|
        sendwert=str(self.resp)
        s_stream=bytes(sendwert,'utf-8')
        conn.send(s_stream)
        sendwert=0

    def Empfangen(self):
#-------------------------------------------------------------------------|
#   Empfangen                                                             |  
#-------------------------------------------------------------------------|
        r_stream = conn.recv(1024)
        self.req = int(r_stream)

    def Empfangsdaten_auswerten(self):
#-------------------------------------------------------------------------|
#   Empfangsdaten auswerten                                               |  
#-------------------------------------------------------------------------|
        global start1, start2, start3a, start3b
        global order1, order2,order3a, order3b
        global hauptbandspeed

        start1 = int((self.req & 2**0) / 2**0)
        start2 = int((self.req & 2**5) / 2**5)
        start3a = int((self.req & 2**10) / 2**10)
        start3b = int((self.req & 2**21) / 2**21)
        order1 = int(((self.req & 2**1)+(self.req & 2**2)+(self.req & 2**3)+(self.req & 2**4))/2**1)
        order2 = int(((self.req & 2**6)+(self.req & 2**7)+(self.req & 2**8)+(self.req & 2**9))/2**6)
        order3a = int(((self.req & 2**11)+(self.req & 2**12)+(self.req & 2**13)+(self.req & 2**14))/2**11)
        order3b = int(((self.req & 2**22)+(self.req & 2**23)+(self.req & 2**24)+(self.req & 2**25))/2**22)
        hauptbandspeed = int((self.req & 2**15) / 2**15)
        self.write_rfid = int((self.req & 2**16) / 2**16)     # erstes bit = 1 : rfid schreiben
        self.read_rfid = int((self.req & 2**17) / 2**17)      # = 1 rfid lesen
        self.read_uid = int((self.req & 2**18) / 2**18)       # = 1 uid lesen
        self.antennen_nr = int((self.req & (2**19 + 2**20)) / 2**19)  # 2 bit antennennummer


    def RFID_Daten(self):
#-------------------------------------------------------------------------|
#   RFID-Daten je nach empfangenem Befehl zumm Senden vorbereiten         |  
#-------------------------------------------------------------------------|
        if self.read_uid != 0:
            #rfid_erkennen() ..wahrscheinlich unnötig, läuft ja in schleife
            produktnr = antenne[self.antennen_nr]
            if produktnr !=0:                                   #wenn ein teil erkannt wurde
                self.resp=self.resp & (((2**32)-1) - 255 * (2**16))
                uid_gefragt = uid[produktnr]
                self.resp=self.resp | (uid_gefragt * 2**16)               #uid wird gesendet
            else:
                uid_gefragt = 0
                self.resp=self.resp & (((2**32)-1) - 255 * (2**16))       #uid aus sendestream löschen
            
        if self.write_rfid != 0:
            #rfid_erkennen()
            produktnr= antenne[self.antennen_nr]
            if produktnr !=0:
                rfiddata = int((self.req & (255 * 2**24)) / 2**24)   #daten für tag aus empfangsstrom filtern
                rfid_tag[produktnr] = rfiddata

        if self.read_rfid != 0:
            #rfid_erkennen()
            produktnr= antenne[self.antennen_nr]
            if produktnr !=0:                                   #wenn ein teil erkannt wurde
                self.resp = self.resp & ((2**32-1) - 255 * 2**24)
                rfiddata = rfid_tag[produktnr]
                self.resp = self.resp | (rfiddata * 2**24)
            else:
                rfiddata = 0
                self.resp = self.resp & ((2**32-1) - 255 * 2**24)
 
    def Anzeige_steuern(self):
#-------------------------------------------------------------------------|
#   Anzeige steuern (abhängig von Handshakesignalen)                      |  
#-------------------------------------------------------------------------|
        if busy1==1:
            twin.itemconfig(Anzeige1.busy, fill="red")
        else:
            twin.itemconfig(Anzeige1.busy, fill="lightgrey")  # lampe für busy
        if ack1==1:
            twin.itemconfig(Anzeige1.ack, fill="red")  # lampe für ack
        else:
            twin.itemconfig(Anzeige1.ack, fill="lightgrey")  # lampe für ack
        if start1==1:
            twin.itemconfig(Anzeige1.start, fill="red")  # lampe für start
        else:
            twin.itemconfig(Anzeige1.start, fill="lightgrey")  # lampe für start
        if busy2==1:
            twin.itemconfig(Anzeige2.busy, fill="red")  # lampe für busy
        else:
            twin.itemconfig(Anzeige2.busy, fill="lightgrey")  # lampe für busy
        if ack2==1:
            twin.itemconfig(Anzeige2.ack, fill="red")  # lampe für ack
        else:
            twin.itemconfig(Anzeige2.ack, fill="lightgrey")  # lampe für ack
        if start2==1:
            twin.itemconfig(Anzeige2.start, fill="red")  # lampe für start
        else:
            twin.itemconfig(Anzeige2.start, fill="lightgrey")  # lampe für start
        if busy3a==1:
            twin.itemconfig(Anzeige3a.busy, fill="red")  # lampe für busy
        else:
            twin.itemconfig(Anzeige3a.busy, fill="lightgrey")  # lampe für busy
        if ack3a==1:
            twin.itemconfig(Anzeige3a.ack, fill="red")  # lampe für ack
        else:
            twin.itemconfig(Anzeige3a.ack, fill="lightgrey")  # lampe für ack
        if start3a==1:
            twin.itemconfig(Anzeige3a.start, fill="red")  # lampe für start
        else:
            twin.itemconfig(Anzeige3a.start, fill="lightgrey")  # lampe für start
        if busy3b==1:
            twin.itemconfig(Anzeige3b.busy, fill="red")  # lampe für busy
        else:
            twin.itemconfig(Anzeige3b.busy, fill="lightgrey")  # lampe für busy
        if ack3b==1:
            twin.itemconfig(Anzeige3b.ack, fill="red")  # lampe für ack
        else:
            twin.itemconfig(Anzeige3b.ack, fill="lightgrey")  # lampe für ack
        if start3b==1:
            twin.itemconfig(Anzeige3b.start, fill="red")  # lampe für start
        else:
            twin.itemconfig(Anzeige3b.start, fill="lightgrey")  # lampe für start


    def RFID_Band_polling(self):
#-------------------------------------------------------------------------|
#   RFID pollen, Band steuern                       |  
#-------------------------------------------------------------------------|      
        RFID1.rfid_erkennen(0)
        RFID2.rfid_erkennen(1)
        RFID3.rfid_erkennen(2)
        
        
        if hauptbandspeed !=0:
            Hauptband.bewege_band()
            band_lief=1


#************************************************************************
#   Objekte erzeugen                                                    *
#************************************************************************



module1=Modul1()
module2=Modul2()
module3a=Modul3a()
module3b=Modul3b()
Stopper1=Stopper(260,360,270,400,1)
Stopper2=Stopper(380,360,390,400,2)
Stopper3=Stopper(410,360,420,400,3)
Stopper4=Stopper(640,360,650,400,4)
Stopper5=Stopper(780,360,790,400,5)
Stopper6=Stopper(810,360,820,400,6)
RFID1=RFID(246,402,265,423)             #Modul1
RFID2=RFID(366,402,385,423)             #Modul2
RFID3=RFID(766,402,785,423)             #Modul3
Sensor1=Sensor(398,370,408,390)         #Modul2(1)
Sensor2=Sensor(428,370,438,390)         #Modul2(2)
Sensor3=Sensor(620,370,630,390)         #Modul3(1) neu ohne Funktion
Sensor4=Sensor(660,370,670,390)         #Modul3(2)
Sensor5=Sensor(794,370,804,390)         #Modul3(3)
Anzeige1=Anzeige(20,280,37,295,str(1))
Anzeige2=Anzeige(300,280,317,295,str(2))
Anzeige3a=Anzeige(590,140,607,155,str(3)+"a")
Anzeige3b=Anzeige(590,625,607,640,str(3)+"b")

Hauptband=Transportband(110,400,890,400)
Querband=Transportband(620,425,820,425)
Kom=Kommunikation()
twin.update()


#************************************************************************
#   Kommunikation mit Leitrechner (evtl. localhost) aufbauen            *
#************************************************************************

while True:
    try:
        PORT = 1601
        HOST = h
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        break
    except:
        print("Verbindung mit Hostrechner noch nicht aufgebaut")
print("Verbindung mit Hostrechner aufgebaut")


#************************************************************************
#   Hauptschleife : Senden/Empfangen -> Bewegen                         *
#************************************************************************

while True:
    time.sleep(0.005)                #Geschwindigkeit Twin
    twin.update()
    Kom.Sendedaten_vorbereiten()
    Kom.Senden()
    Kom.Empfangen()
    Kom.Empfangsdaten_auswerten()
    Kom.RFID_Daten()
    Kom.Anzeige_steuern()
    Kom.RFID_Band_polling()
    twin.update()
    module1.Bewegungsablauf()
    module2.Bewegungsablauf()
    module3a.Bewegungsablauf()
    module3b.Bewegungsablauf()

    
#-------------------------------------------------------------------------|
#   Grafik erneuern (in Schleife)                                         |  
#-------------------------------------------------------------------------|        
    twin.update()





