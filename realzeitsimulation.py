from threading import Thread
from _thread import start_new_thread
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

    """start_new_thread(baker)
    start_new_thread(butcher)
    start_new_thread(cheese)
    start_new_thread(checkout)"""
def sleeper(i):
    print ("thread %d sleeps" %i)
    time.sleep(5)
    print ("thread %d woke up" % i)


for i in range(10):
    t = Thread(target=sleeper, args=(i,))
    t.start()


