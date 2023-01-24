from twinLib2022_v22_12 import PlcModule, ErpConnect


class Anlage(PlcModule):
    def __init__(self):
        super().__init__()
        self.StartBand()
        self.ist_frei = 0


    def handshake(self, order_number : int, module : str) -> None:
        state = 0
        while(True):
            if state == 0 and self.ist_frei == 0:
                if self.ReadOPCTag(module, "Ready"):
                    self.WriteOPCTag(module, "Order", order_number)
                    self.WriteOPCTag(module, "Start", 1)
                    self.ist_frei = 1
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
                    self.ist_frei = 0
                    break


    def bestellung(self, order_number : int) -> None:
        modul = "module1"
        self.handshake(order_number, modul)


    def bauen(self, order_number : int) -> None:
        modul = "module2"
        self.handshake(order_number, modul)


    def lager_1(self, order_number : int) -> None:
        modul = "module3"
        self.handshake(order_number, modul)


    def lager_2(self , order_number : int) -> None:
        modul = "module3b"
        self.handshake(order_number, modul)


anlage = Anlage()
                

    
def Fertigung(bestellung, bauen, lager):
    anlage.bestellung(order_number = bestellung)
    anlage.bauen(order_number = bauen)
    anlage.lager_1(order_number = lager)


for i in range(5):
    order_1 = int(input("Welche Bestellung?: "))
    order_2 = int(input("Bauen: "))
    order_3 = int(input("Lager:"))
    
    Fertigung(order_1, order_2, order_3)


