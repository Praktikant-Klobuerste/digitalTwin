from handshake import Anlage

anlage = Anlage()
                

    


for i in range(5):
    order_1 = input("Welche Bestellung?: ")
    order_2 = input("Bauen: ")
    order_3 = input("Lager:")
    
    anlage.Fertigung(order_1, order_2, order_3)


