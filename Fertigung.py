import numpy as np
from handshake import Anlage
import time

anlage = Anlage()

def convert(x):
    liste = [x[0],x[2],x[4]] # ['1;2;3'] → ['1','2','3']
    _liste = [int(x) for x in liste] # [1, 2, 3]
    return _liste

try:
    with open("./digitalTwin/bestellung.csv", "r") as file:

        bestellung = [i.strip() for i in file.readlines()]
        bestellung.pop(0) # Spalten Überschrift entfernt
        print(bestellung)
except FileNotFoundError: 
    print("Ich mag kleine 🖐")


else:
    bestellung += ["0;0;0"] # Zum verschieben am Ende Zwei leere Aufträge
    bestellung += ["0;0;0"]
    conv_bestellung = [convert(reihe) for reihe in bestellung]
    np_bestellung = np.array(conv_bestellung)

    np_bestellung[1:, 1] = np_bestellung[:-1, 1]
    np_bestellung[1:, 2] = np_bestellung[:-1, 2]
    np_bestellung[1:, 2] = np_bestellung[:-1, 2]
    np_bestellung[0, 1] = 0
    np_bestellung[0, 2] = 0
    np_bestellung[1, 2] = 0

    print(np_bestellung)

    for i in range(len(np_bestellung)):


        anlage.Fertigung(np_bestellung[i][0], np_bestellung[i][1], np_bestellung[i][2])
        print(i) 

    time.sleep(5)
    anlage.StopBand()