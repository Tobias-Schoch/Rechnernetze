import itertools
from heapq import heappush, heappop
from typing import List, Any

heap = []  # Zeitpunkt, Prio, Nr, Funktion
counter = itertools.count()


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
        if self.Warteschlange[0] == Kundename:
            return True
        return False

    def remove(self, Kunde):
        if len(self.Warteschlange) == 1 and self.Warteschlange.count(Kunde.Name) > 0:
            self.bEmpty = 0
            self.Warteschlange.remove(Kunde.Name)
        elif len(self.Warteschlange) > 1 and self.Warteschlange.count(Kunde.Name) > 0:
            self.Warteschlange.remove(Kunde.Name)


Theken = []
Theken.append(Station(10, [], "Bäcker"))
Theken.append(Station(60, [], "Käse"))
Theken.append(Station(30, [], "Metzger"))
Theken.append(Station(5, [], "Kasse"))

