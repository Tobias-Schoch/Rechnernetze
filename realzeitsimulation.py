from threading import Thread
import time
from threading import Event
from threading import Lock
import datetime

class Station(Thread):
    def __init__(self, name, dauer, length):
        self.name = name
        self.dauer = dauer
        self.length = length

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

