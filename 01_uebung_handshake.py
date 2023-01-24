from twinLib2022_v22_12 import PlcModule, ErpConnect


class Anlage(PlcModule):
    def __init__(self):
        super().__init__()
        self.StartBand()
        self.sub_state = 0

    def bestellung(self, order_number : int) -> None:
        state = 0
        while(True):
            if state == 0 and self.sub_state == 0:
                if self.ReadOPCTag("module1", "Ready"):
                    self.WriteOPCTag("module1", "Order", order_number)
                    self.WriteOPCTag("module1", "Start", 1)
                    state = 1

            elif state == 1:
                if self.ReadOPCTag("module1", "Acknowledge"):
                    self.WriteOPCTag("module1", "Start", 0)
                    state = 2

            elif state == 2:
                if self.ReadOPCTag("module1", "Acknowledge") == False:
                    state = 3
            elif state == 3:
                if self.ReadOPCTag("module1", "Busy") == False:
                    state = 0
                    self.sub_state = 1
                    break

    def bauen(self, order_number : int):
        state = 0
        while(True):
            if state == 0 and self.sub_state == 1:
                if self.ReadOPCTag("module2", "Ready"):
                    self.WriteOPCTag("module2", "Order", order_number)
                    self.WriteOPCTag("module2", "Start", 1)
                    state = 1

            elif state == 1:
                if self.ReadOPCTag("module2", "Acknowledge"):
                    self.WriteOPCTag("module2", "Start", 0)
                    state = 2

            elif state == 2:
                if self.ReadOPCTag("module2", "Acknowledge") == False:
                    state = 3
            elif state == 3:
                if self.ReadOPCTag("module2", "Busy") == False:
                    state = 0
                    self.sub_state = 2
                    break

    def lager(self, modulwahl, order_number : int):
        
        modul = f"module{modulwahl}"
        print(modul)

        state = 0
        while(True):
            if state == 0 and self.sub_state == 2:
                if self.ReadOPCTag(modul, "Ready"):
                    self.WriteOPCTag(modul, "Order", order_number)
                    self.WriteOPCTag(modul, "Start", 1)
                    state = 1

            elif state == 1:
                if self.ReadOPCTag(modul, "Acknowledge"):
                    self.WriteOPCTag(modul, "Start", 0)
                    state = 2

            elif state == 2:
                if self.ReadOPCTag(modul, "Acknowledge") == False:
                    state = 3
            elif state == 3:
                if self.ReadOPCTag(modul, "Busy") == False:
                    state = 0
                    self.sub_state = 0
                    break


anlage = Anlage()
                

    
def Fertigung(bestellung, bauen, lager):
    anlage.bestellung(order_number = bestellung)
    anlage.bauen(order_number = bauen)
    anlage.lager(modulwahl="3b", order_number = lager)


for i in range(5):
    order_1 = int(input("Welche Bestellung?: "))
    order_2 = int(input("Bauen: "))
    order_3 = int(input("Lager:"))
    
    Fertigung(order_1, order_2, order_3)


