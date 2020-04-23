import itertools
from heapq import heappush, heappop
from typing import List, Any

heap = []  # Zeitpunkt, Prio, Nr, Funktion
counter = itertools.count()

# Output Text Declare
UserDoc = open('supermarkt_customer.txt', 'w+')
stationDoc = open('supermarkt_station.txt', 'w+')
supermarktDoc = open('supermarkt.txt', 'w+')


# print("Test", file=UserDoc)


class Station:

    def __init__(self, Dauer, Liste, name="leer", bEmpty=0):
        self.Warteschlange = Liste
        self.Name = name
        self.bEmpty = bEmpty
        self.Dauer = Dauer

    def isEmpty(self):
        return self.bEmpty

    def add(self, Kunde):
        self.bEmpty = 1
        self.Warteschlange.append(Kunde.Name)

    def isMyTurn(self, Kundename):
        if (self.Warteschlange[0] == Kundename):
            return True
        return False

    def remove(self, Kunde):
        if (len(self.Warteschlange) == 1 and self.Warteschlange.count(Kunde.Name) > 0):
            self.bEmpty = 0
            self.Warteschlange.remove(Kunde.Name)
        elif (len(self.Warteschlange) > 1 and self.Warteschlange.count(Kunde.Name) > 0):
            self.Warteschlange.remove(Kunde.Name)


Theken = []
# Theke[0] = Baecker, [1] = kaese, [2] = Wurst, [3] = kasse
Theken.append(Station(10, [], "Bäcker"))
Theken.append(Station(60, [], "Käse"))
Theken.append(Station(30, [], "Metzger"))
Theken.append(Station(5, [], "Kasse"))


class User:
    def __init__(self, TypInformation, Name=""):
        self.Name = Name
        self.Position = -1
        self.Laufen = TypInformation[0]
        self.WarteschlangeMax = TypInformation[1]
        self.KaufeAnzahl = TypInformation[2]

    def anzahlDerEinkaeufe(self):
        return len(self.Laufen)

    def getPosition(self):
        return self.Position

    def incPosition(self):
        self.Position += 1

    def walk(self):
        print(self.Name, self.Position, len(self.Laufen))
        return self.Laufen[self.Position]

    def getWarteschlangeMax(self):
        if (self.Position < self.anzahlDerEinkaeufe()):
            return self.WarteschlangeMax[self.Position]
        else:
            return -1


class Ordering:
    def __init__(self, ):
        self.Prio = 1

    def __lt__(self, other):
        return True


class Supermarkt:
    AnzahlDerKunden = 0
    Zeit = 0
    A = 200
    B = 60

    # TypInfo: 4xLaufweg, 4xMaxWarteschlabnge, 4xMengeArtikel.
    # Baecker, Kaese, Wurst, Kasse
    TypInfoA = ([10, 30, 45, 60], [11, 11, 6, 21], [10, 5, 3, 30])

    # TypInfo: 3xLaufweg, 3xMaxWarteschlabnge, 3xMengeArtikel.
    # Wurst, Kasse, Baecker
    TypInfoB = ([30, 30, 20], [6, 21, 21], [2, 3, 3])

    def start(self):
        # init 10 Kunden von Typ1 und 30 Kunden von Typ2
        UserA1 = User(self.TypInfoA, "A1")
        UserB1 = User(self.TypInfoB, "B1")
        UserA2 = User(self.TypInfoA, "A2")
        UserB2 = User(self.TypInfoB, "B2")
        UserA3 = User(self.TypInfoA, "A3")
        UserB3 = User(self.TypInfoB, "B3")
        UserA4 = User(self.TypInfoA, "A4")
        UserB4 = User(self.TypInfoB, "B4")
        UserA5 = User(self.TypInfoA, "A5")
        UserB5 = User(self.TypInfoB, "B5")

        UserA6 = User(self.TypInfoA, "A6")
        UserB6 = User(self.TypInfoB, "B6")
        UserA7 = User(self.TypInfoA, "A7")
        UserB7 = User(self.TypInfoB, "B7")
        UserA8 = User(self.TypInfoA, "A8")
        UserB8 = User(self.TypInfoB, "B8")
        UserA9 = User(self.TypInfoA, "A9")
        UserB9 = User(self.TypInfoB, "B9")
        UserA10 = User(self.TypInfoA, "A10")
        UserB10 = User(self.TypInfoB, "B10")

        UserB11 = User(self.TypInfoB, "B11")
        UserB12 = User(self.TypInfoB, "B12")
        UserB13 = User(self.TypInfoB, "B13")
        UserB14 = User(self.TypInfoB, "B14")
        UserB15 = User(self.TypInfoB, "B15")
        UserB16 = User(self.TypInfoB, "B16")
        UserB17 = User(self.TypInfoB, "B17")
        UserB18 = User(self.TypInfoB, "B18")
        UserB19 = User(self.TypInfoB, "B19")
        UserB20 = User(self.TypInfoB, "B20")

        UserB21 = User(self.TypInfoB, "B21")
        UserB22 = User(self.TypInfoB, "B22")
        UserB23 = User(self.TypInfoB, "B23")
        UserB24 = User(self.TypInfoB, "B24")
        UserB25 = User(self.TypInfoB, "B25")
        UserB26 = User(self.TypInfoB, "B26")
        UserB27 = User(self.TypInfoB, "B27")
        UserB28 = User(self.TypInfoB, "B28")
        UserB29 = User(self.TypInfoB, "B29")
        UserB30 = User(self.TypInfoB, "B30")

        # alle Kunden auf den heap setzen.
        add_Task(0, UserA1, walk, [0, 2, 1, 3])
        add_Task(200, UserA2, walk, [0, 2, 1, 3])
        add_Task(400, UserA3, walk, [0, 2, 1, 3])
        add_Task(600, UserA4, walk, [0, 2, 1, 3])
        add_Task(800, UserA5, walk, [0, 2, 1, 3])
        add_Task(1000, UserA6, walk, [0, 2, 1, 3])
        add_Task(1200, UserA7, walk, [0, 2, 1, 3])
        add_Task(1400, UserA8, walk, [0, 2, 1, 3])
        add_Task(1600, UserA9, walk, [0, 2, 1, 3])
        add_Task(1800, UserA10, walk, [0, 2, 1, 3])

        add_Task(1, UserB1, walk, [2, 3, 0])
        add_Task(61, UserB2, walk, [2, 3, 0])
        add_Task(121, UserB3, walk, [2, 3, 0])
        add_Task(181, UserB4, walk, [2, 3, 0])
        add_Task(241, UserB5, walk, [2, 3, 0])
        add_Task(301, UserB6, walk, [2, 3, 0])
        add_Task(361, UserB7, walk, [2, 3, 0])
        add_Task(421, UserB8, walk, [2, 3, 0])
        add_Task(481, UserB9, walk, [2, 3, 0])
        add_Task(541, UserB10, walk, [2, 3, 0])
        add_Task(601, UserB11, walk, [2, 3, 0])
        add_Task(661, UserB12, walk, [2, 3, 0])
        add_Task(721, UserB13, walk, [2, 3, 0])
        add_Task(781, UserB14, walk, [2, 3, 0])
        add_Task(841, UserB15, walk, [2, 3, 0])

        add_Task(901, UserB16, walk, [2, 3, 0])
        add_Task(961, UserB17, walk, [2, 3, 0])
        add_Task(1021, UserB18, walk, [2, 3, 0])
        add_Task(1081, UserB19, walk, [2, 3, 0])
        add_Task(1141, UserB20, walk, [2, 3, 0])
        add_Task(1201, UserB21, walk, [2, 3, 0])
        add_Task(1261, UserB22, walk, [2, 3, 0])
        add_Task(1321, UserB23, walk, [2, 3, 0])
        add_Task(1381, UserB24, walk, [2, 3, 0])
        add_Task(1441, UserB25, walk, [2, 3, 0])
        add_Task(1501, UserB26, walk, [2, 3, 0])
        add_Task(1561, UserB27, walk, [2, 3, 0])
        add_Task(1621, UserB28, walk, [2, 3, 0])
        add_Task(1681, UserB29, walk, [2, 3, 0])
        add_Task(1741, UserB30, walk, [2, 3, 0])

        self.EventHandler()

    def EventHandler(self):
        while (heap):
            # hol den nachsten kunden von der heapqueue
            Zeit, Prio, count, Kunde, func, order = heappop(heap)  #
            # arbeite die aktion des kunden ab(laufen/kaufen/warten)

            tZeit, tfunc, msg = func(Kunde, order)
            if (msg != ""):
                UserDoc.write(str(Zeit) + ":" + msg + "\n")
                print(Theken[0].Warteschlange)
            # kunde nur in die queue wieder reinsetzten wenn func nicht end ist
            if (tfunc != leave):
                # berechne wann der kunde wieder eine aktion ausführen will
                Zeit = Zeit + tZeit
                # print(Kunde.Name ,Zeit, tfunc)
                # setze den kunden wieder auf die heapque
                add_Task(Zeit, Kunde, tfunc, order)
                # "debug" pfusch am bau
                if (tfunc != wait):
                    a = 8  # print(Zeit - tZeit, ":", Kunde.Name, tfunc, Prio, count) #
            else:  # Fertige Kunden
                print(Kunde.Name, Zeit + tZeit, tZeit, tfunc)
                leave()

        # Statistic Print's after Symulation
        else:
            print("Simulationsende      : " + str(Zeit) + "s", file=supermarktDoc)
            supermarktDoc.write("Simulationsende      : " + str(Zeit) + "s")
            #        supermarktDoc.write("Kunden               : " + str(AnzahlDerKunden))
            #        print("Einkäufe             : " + str(), file=supermarktDoc)
            #        print("Mittlere Einkaufszeit: " + str(), file=supermarktDoc)
            #        print("Mittlere Einkaufszeit (vollständig): " + str(), file=supermarktDoc)
            #        print("Drop percentage at Bäcker    : " + str(), file=supermarktDoc)
            #        print("Drop percentage at Metzger   : " + str(), file=supermarktDoc)
            #        print("Drop percentage at Käse      : " + str(), file=supermarktDoc)
            #        print("Drop percentage at Kasse     : " + str(), file=supermarktDoc)

            # Closing Writing Streams from Statistic Documents
            UserDoc.close()
            stationDoc.close()
            supermarktDoc.close()


def add_Task(Zeit, TypInfo, tfunc, order):
    count = next(counter)
    Prio = 3
    if (tfunc == walk):
        Prio = 0
    elif (tfunc == entry):
        Prio = 2
    else:
        Prio = 1
    eantry = [Zeit, Prio, count, TypInfo, tfunc, order]
    # print(TypInfo.Name, tfunc)
    heappush(heap, eantry)


#############################################################
#       funktionen die abgelaufen werden vom kunden         #
#############################################################
#   wenn kunde von station zu station will      #
#################################################
def walk(Kunde, order):
    msg = ""
    if (Kunde.getPosition() != -1):
        msg = (Kunde.Name + " Finished at " + Theken[order[Kunde.getPosition()]].Name)
        Theken[order[Kunde.getPosition()]].remove(Kunde)
    Kunde.incPosition()
    return Kunde.walk(), entry, msg


#################################################
#   kunde wartet an der station                 #
#################################################
def wait(Kunde, order):
    if (Theken[order[Kunde.getPosition()]].isMyTurn(Kunde.Name)):
        zeit, func, msg = service(Kunde, order)
        return zeit, func, msg
    else:
        return 1, wait, ""  # Theken[order[Kunde.getPosition()]].Dauer


#################################################
#   kunde kommt an der sation an                #
#################################################
def entry(Kunde, order):
    if (Kunde.getWarteschlangeMax() > len(Theken[order[Kunde.getPosition()]].Warteschlange)):
        msg = (Kunde.Name + " Queueing at " + Theken[order[Kunde.getPosition()]].Name)
        if (Theken[order[Kunde.getPosition()]].bEmpty == 0):
            Theken[order[Kunde.getPosition()]].add(Kunde)
            zeit, func, msgtmp = service(Kunde, order)
            return (zeit, func, msg)
        else:
            Theken[order[Kunde.getPosition()]].add(Kunde)
            zeit, func, msgtmp = wait(Kunde, order)
            return (zeit, func, msg)
    else:
        # Kunde.incPosition()
        msg = (Kunde.Name + " Dropped at " + Theken[order[Kunde.getPosition()]].Name)
        zeit, func, msgtmp = walk(Kunde, order)
        return (zeit, func, msg)


#################################################
#   kunde ist feritg mit den einkauf            #
#################################################
def end(Kunde, order):
    # print("end")
    msg = (Kunde.Name + " Finished at " + Theken[order[Kunde.getPosition()]].Name)
    Theken[order[Kunde.getPosition()]].remove(Kunde)
    return 9999, leave, msg


def leave():
    return 0


#################################################
#   kunde wird an einer station bedient         #
#################################################
def service(Kunde, order):
    # TODO: Kunde aus der Warteschlange der Station nehmen
    if ((Kunde.anzahlDerEinkaeufe() - 1) == Kunde.getPosition()):
        return Theken[order[Kunde.getPosition()]].Dauer * Kunde.KaufeAnzahl[Kunde.getPosition()], end, ""
    else:
        tmp = Theken[order[Kunde.getPosition()]].Dauer * Kunde.KaufeAnzahl[Kunde.getPosition()]
        # print(Kunde.Name, Theken[order[Kunde.getPosition()]].Dauer ,tmp, Theken[order[Kunde.getPosition()]].Name)
        return tmp, walk, ""


#############################################################
#           Programmstart! supermarkt wird geoefnnet        #
#############################################################
a = Supermarkt()
a.start()