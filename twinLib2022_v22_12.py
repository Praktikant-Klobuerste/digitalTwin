import socket
import time
import threading

#****************diese beiden Zeilen aktivieren, wenn Sie die httpdlib2 installiert haben***********#
import httplib2 as protokoll                                                                       #
import xml.etree.ElementTree as xml                                                                #
#***************************************************************************************************#


class PlcModule:

    def __init__(self):
        #*******************************************************************************************#
        # Bei Betrieb mit zwei Rechnern hier die IP durch die IP des Rechners ersetzen, auf         #
        # dem der twin läuft :                                                                       #
        #                                                                                           #
        HOST = '192.168.2.198'
        #HOST = '192.168.178.89'
        #
        #                                                                                           #
        #*******************************************************************************************#
        PORT = 1601                #port
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))     
        self.req=0
        global apfel
        global bandlauf
        bandlauf = 0
        def plapper():
            global bandlauf
            while True:
                #empfangen-----------
                r_stream = self.s.recv(1024)
                self.resp = int(r_stream)
                #senden--------------
                if bandlauf == 1:
                    self.req=self.req | 2**15           #band an
                else:
                    self.req=self.req  & ((2**32-1) - 2**15)
                sendwert = str(self.req)
                s_stream = bytes(sendwert,'utf-8')
                self.s.send(s_stream)                
        apfel=threading.Thread(target=plapper, args=())
        apfel.start()
       
    def ReadRFIDUID(self,antenna):
        #vorlauf, weil fürs lesen die kommunikationsreihenfolge falsch+++++
        #empfangen-----------
        r_stream = self.s.recv(1024)
        self.resp = int(r_stream)       #resp ("response") ist wert vom twin
        #senden--------------
        self.req = self.req & ((2**32-1) - 2**16 - 2**17 - 2**18- 2**19 - 2**20)    #alles null
        self.req = self.req | (antenna * 2**19)     # antennennummer
        self.req = self.req | 2**18                 #flag für "read uid"
        sendwert = str(self.req)
        s_stream = bytes(sendwert,'utf-8')          #senden
        self.s.send(s_stream)
        self.req = self.req & (((2**32)-1) - 2**18)    #alles null
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #empfangen-----------
        r_stream = self.s.recv(1024)
        self.resp = int(r_stream)       #resp ("response") ist wert vom twin
        #print("uid empfangen roh : ",self.resp)
        #senden--------------
        self.req = self.req & ((2**32-1) - 2**16 - 2**17 - 2**18- 2**19 - 2**20)    #alles null
        self.req = self.req | (antenna * 2**19)     # antennennummer
        self.req = self.req | 2**18                 #flag für "read uid"
        sendwert = str(self.req)
        s_stream = bytes(sendwert,'utf-8')          #senden
        self.s.send(s_stream)
        self.req = self.req & (((2**32)-1) - 2**18)    #alles null        
        #auswerten-------------------------------
        uidwert = int((self.resp & (255 * 2**16)) / 2**16)     # Byte 3
        return(uidwert)
       
    def ReadRFIDTag(self,antenna):
        #vorlauf, weil fürs lesen die kommunikationsreihenfolge falsch+++++
        r_stream = self.s.recv(1024)
        #print("rec = ",r_stream)
        self.resp = int(r_stream)
        #senden--------------
        self.req = self.req | (antenna * 2**19) # antennennummer
        self.req = self.req | 2**17     #flag für "read data"
        sendwert = str(self.req)
        s_stream = bytes(sendwert,'utf-8')
        self.s.send(s_stream)
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #empfangen-----------
        r_stream = self.s.recv(1024)
        self.resp = int(r_stream)
        #senden--------------
        self.req = self.req | (antenna * 2**19) # antennennummer
        self.req = self.req | 2**17     #flag für "read data"
        sendwert = str(self.req)
        s_stream = bytes(sendwert,'utf-8')
        self.s.send(s_stream)
        self.req = self.req & (((2**32)-1) - 2**17 )
        #auswerten-------------------------------
        tagdata = int((self.resp & (2**24 * 255)) / 2**24)      # Byte 4   
        return(tagdata)     

    def WriteRFIDTag(self,antenna,data):
        #empfangen-----------
        r_stream = self.s.recv(1024)
        self.resp = int(r_stream)
        #senden--------------
        self.req = self.req | (antenna * 2**19) # antennennummer
        self.req = self.req | 2**16             #flag für "write data"
        self.req = self.req | (data * 2**24)
        sendwert = str(self.req)
        s_stream = bytes(sendwert,'utf-8')
        self.s.send(s_stream)
        #self.req = self.req & (((2**32-1)) - 2**16 )
        self.req = self.req & (((2**32-1)) - 2**16 - 255 * 2**24 )
        #auswerten-------------------------------

    def StartBand(self):
        global apfel
        global bandlauf
        bandlauf = 1

    def StopBand(self):
        global apfel
        global bandlauf
        bandlauf = 0


    def ReadOPCTag(self,module, tag):
        #empfangen-----------
        r_stream = self.s.recv(1024)
        self.resp = int(r_stream)
        #senden--------------
        sendwert = str(self.req)
        s_stream = bytes(sendwert,'utf-8')
        self.s.send(s_stream)
        #auswerten-------------------------------
        if module=="module1":
            if tag=="Ready":
                return(int((self.resp & 2**0)))
            if tag=="Busy":
                return(int((self.resp & 2**2)/2**2))
            if tag=="Acknowledge":
                return(int((self.resp & 2**1)/2**1))
            if tag=="Message":
                return(int((self.resp & 2**9) + (self.resp & 2**10)) / 2**9) #kanban
        if module=="module2":
            if tag=="Ready":
                return(int((self.resp & 2**3)/2**3))
                #return(1)
            if tag=="Busy":
                return(int((self.resp & 2**5)/2**5))
            if tag=="Acknowledge":
                return(int((self.resp & 2**4)/2**4))
        if module=="module3":
            if tag=="Ready":
                return(int((self.resp & 2**6)/2**6))
                #return(1)
            if tag=="Busy":
                return(int((self.resp & 2**8)/2**8))
            if tag=="Acknowledge":
                return(int((self.resp & 2**7)/2**7))
            if tag=="Message":
                return(int((self.resp & 2**11) + (self.resp & 2**12)) / 2**11) #sensoren
        if module=="module3b":
            if tag=="Ready":
                return(int((self.resp & 2**13)/2**13))
                #return(1)
            if tag=="Busy":
                return(int((self.resp & 2**14)/2**14))
            if tag=="Acknowledge":
                return(int((self.resp & 2**15)/2**15))
            

    def WriteOPCTag(self,module,tag,value):
            #empfangen-----------
            r_stream = self.s.recv(1024)
            self.resp = int(r_stream)
            #sendedaten-vorbereiten------------------------------
            if module=="module1":
                if tag=="Start":
                    if value==1:
                        self.req=self.req | 2**0
                    else:
                        self.req=self.req & ((2**32-1) - 2**0)
                if tag=="Order":
                    self.req=self.req & ((2**32-1) - 2**1 - 2**2 - 2**3- 2**4)                
                    if value==1:
                        self.req=self.req | 2**1
                    if value==2:
                        self.req=self.req | 2**2
                    if value==3:
                        self.req=self.req | 2**1
                        self.req=self.req | 2**2
                    if value==4:
                        self.req=self.req | 2**3
                    if value==10:
                        self.req=self.req | 2**2
                        self.req=self.req | 2**4
                        
            if module=="module2":
                if tag=="Start":
                    if value==1:
                        self.req=self.req | 2**5
                    else:
                        self.req=self.req & ((2**32-1) - 2**5)
                if tag=="Order":
                    self.req=self.req & ((2**32-1) - 2**6 - 2**7 - 2**8- 2**9)                
                    if value==1:
                        self.req=self.req | 2**6
                    if value==2:
                        self.req=self.req | 2**7
                    if value==3: 
                        self.req=self.req | 2**6 | 2**7
                    if value==4: 
                        self.req=self.req | 2**8
                    if value==5:
                        self.req=self.req | 2**6 | 2**8
                    if value==6:
                        self.req=self.req | 2**7 | 2**8
                    if value==10:
                        self.req=self.req | 2**7
                        self.req=self.req | 2**9

            if module=="module3":
                if tag=="hauptbandspeed":
                    if value!=0:
                        self.req=self.req | 2**15
                    else:
                        self.req=self.req & ((2**32-1) - 2**15)                        
                if tag=="Start":
                    if value==1:
                        self.req=self.req | 2**10
                    else:
                        self.req=self.req & ((2**32-1) - 2**10)
                if tag=="Order":
                    self.req=self.req & ((2**32-1) - 2**11 - 2**12 - 2**13- 2**14)                
                    if value==1:
                        self.req=self.req | 2**11
                    if value==2:
                        self.req=self.req | 2**12
                    if value==3:
                        self.req=self.req | 2**11
                        self.req=self.req | 2**12
                    if value==4:
                        self.req=self.req | 2**13
                    if value==5:
                        self.req=self.req | 2**13 | 2**11
                    if value==6:
                        self.req=self.req | 2**13 | 2**12
                    if value==7:
                        self.req=self.req | 2**13 | 2**12| 2**11
                    if value==8:
                        self.req=self.req | 2**14
                    if value==9:
                        self.req=self.req | 2**14 | 2**11                        
                    if value==10:
                        self.req=self.req | 2**12
                        self.req=self.req | 2**14
                    if value==12:
                        self.req=self.req | 2**13
                        self.req=self.req | 2**14

            if module=="module3b":  #**********************************************************                        
                if tag=="Start":
                    if value==1:
                        self.req=self.req | 2**21
                    else:
                        self.req=self.req & ((2**32-1) - 2**21) #nimmt startzurück
                if tag=="Order":
                    self.req=self.req & ((2**32-1) - 2**22 - 2**23) #nimmtorder zurück               
                    if value==1:
                        self.req=self.req | 2**22
                    if value==2:
                        self.req=self.req | 2**23
                    if value==3:
                        self.req=self.req | 2**22
                        self.req=self.req | 2**23#*********************************************
                    if value==12:
                        self.req=self.req | 2**24
                        self.req=self.req | 2**25
            #senden--------------
            sendwert = str(self.req)
            s_stream = bytes(sendwert,'utf-8')
            self.s.send(s_stream)
            


class ErpConnect: 

    def __init__(self):
        self.quelle = protokoll.Http()

    #def ReadERPPart(self,basename,id,part):
    def ReadERPPart(self,id,part):
        if part == 'top':
            part= 'teil3'
        if part == 'middle':
            part = 'teil2'
        if part == 'bottom':
            part= 'teil1'        
        id = str(id)
        #x = self.quelle.request("https://brunello.ts-muenchen.de/"+basename+"/get_auftrag.php?id="+id)[1]                                                           
        x = self.quelle.request("https://informatik-ts-muenchen.de/AIT/get_auftrag.php?id="+id)[1]
        
        root = xml.fromstring(x)
        item = root.find(part)
        teil = int(item.text)
        return(teil)

    #def ReadERPProductDone(self,basename,id):
    def ReadERPProductDone(self,id):
        id = str(id)
        x = self.quelle.request("https://informatik-ts-muenchen.de/AIT/get_auftrag.php?id="+id)[1]                                                           
        root = xml.fromstring(x)
        item = root.find('done')
        wert = item.text
        return(wert)

    #def ReadERPExists(self,basename,id):
    def ReadERPExists(self,id):
        id = str(id)
        x = self.quelle.request("https://informatik-ts-muenchen.de/AIT/get_auftrag.php?id="+id)[1]                                                           
        root = xml.fromstring(x)
        item = root.find('error')
        fehler = int(item.text)
        return(fehler)

    #def SetERPProductDone(self,basename,id):
    def SetERPProductDone(self,id):
        id = str(id)
        x = self.quelle.request("https://informatik-ts-muenchen.de/AIT/set_done.php?id="+id)        

    #def ResetERPProductDone(self,basename,id):
    def ResetERPProductDone(self,id):
        id = str(id)
        x = self.quelle.request("https://informatik-ts-muenchen.de/AIT/reset_done.php?id="+id) 

    #def ResetERPAllProductsDone(self,basename):
    def ResetERPAllProductsDone(self):
        produkt=0
        error=0
        while error==0:
            x = self.quelle.request("https://informatik-ts-muenchen.de/AIT/reset_done.php?id="+str(produkt))
            produkt=produkt+1
            x = self.quelle.request("https://informatik-ts-muenchen.de/AIT/get_auftrag.php?id="+str(produkt))[1]                                                           
            root = xml.fromstring(x)
            item = root.find('error')
            error = int(item.text)
                    
    #def ChangeERPSequence(self,basename,id1,id2):
    def ChangeERPSequence(self,id1,id2):
        id1 = str(id1)
        id2 = str(id2)
        x = self.quelle.request("ttps://informatik-ts-muenchen.de/AIT/swap_id.php?id_alt="+id1+"&id_neu="+id2)


