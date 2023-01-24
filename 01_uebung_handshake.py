from twinLib2022_v22_12 import PlcModule, ErpConnect
import random

class Anlage(PlcModule):
    def __init__(self):
        super().__init__()
        self.StartBand()
        self.ist_frei = False


    def handshake(self, order_number : int, module : str) -> bool:
        state = 0
        if state == 0 and self.ist_frei == False:
            if self.ReadOPCTag(module, "Ready"):
                self.WriteOPCTag(module, "Order", order_number)
                self.WriteOPCTag(module, "Start", 1)
                self.ist_frei = True
                state = 1

        elif state == 1:
            if self.ReadOPCTag(module, "Acknowledge"):
                self.WriteOPCTag(module, "Start", 0)
                state = 2

        elif state == 2:
            if self.ReadOPCTag(module, "Acknowledge") == False:
                state = 3

        elif state == 3:
            if self.ReadOPCTag(module, "Busy") == False:
                state = 0
                self.ist_frei = False
                
        return self.ist_frei



    def bestellung(self, order_number : int) -> bool:
        modul = "module1"
        return self.handshake(order_number, modul)


    def bauen(self, order_number : int) -> bool:
        modul = "module2"
        return self.handshake(order_number, modul)


    def lager_1(self, order_number : int) -> bool:
        modul = "module3"
        return self.handshake(order_number, modul)


    def lager_2(self , order_number : int) -> bool:
        modul = "module3b"
        return self.handshake(order_number, modul)


anlage = Anlage()
                

    
def serielle_Fertigung(bestellung, bauen, lager):
    while(anlage.ist_frei == False):
        anlage.bestellung(order_number = bestellung)

    while(anlage.ist_frei == False):
        anlage.bauen(order_number = bauen)

    while(anlage.ist_frei == False):
        anlage.lager_1(order_number = lager)


def redunante_Fertigung():
    anlage.bestellung(1)
    anlage.bauen(random.randint(1, 2))
    anlage.lager_1(random.randint(1, 3))

    anlage.bestellung(2)
    anlage.bauen(random.randint(1, 2))
    anlage.lager_2(random.randint(1, 3))


def starre_Fertigung(bestellung, bauen, lager):
    anlage.bestellung(order_number = bestellung)
    anlage.bauen(order_number=bauen)
    anlage.lager_1(order_number=lager)





for i in range(5):
    order_1 = int(input("Welche Bestellung?: "))
    order_2 = int(input("Bauen: "))
    order_3 = int(input("Lager:"))
    
    serielle_Fertigung(order_1, order_2, order_3)


