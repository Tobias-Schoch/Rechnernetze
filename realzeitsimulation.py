from threading import Thread
import time
from threading import Event
from threading import Lock
import datetime

class Store(Thread):
    def __init__(self, name, dauer):
        self.name = name
        self.dauer = dauer

class Customer(Thread):
    def __init__(self, name, todo):
        self.name = name
        self.todo = list(todo)
        self.actual_todo = self.todo.pop(0)
        self.skipped_todo = []
        self.start = datetime.datetime.now()
        self.finish = 0

def generate_customer(sleep, name, todo):
    # TODO: generater customer

if __name__ == "__main__":
    baker = Store("Bäcker", 10)
    butcher = Store("Metzger", 30)
    cheese = Store("Käsetheke", 60)
    checkout = Store("Kasse", 5)

    baker.start()
    butcher.start()
    cheese.start()
    checkout.start()
