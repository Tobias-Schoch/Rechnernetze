from threading import Thread
from _thread import start_new_thread
import time
from threading import Event
from threading import Lock
import datetime

class Station(Thread):
    def __init__(self, name, dauer):
        Thread.__init__(self)
        self.name = name
        self.dauer = dauer
        self.stop = Event()

    #def run(self):
        #while not

class Customer(Thread):
    def __init__(self, name, todo):
        Thread.__init__(self)
        self.name = name
        self.todo = list(todo)
        self.actual_todo = self.todo.pop(0)
        self.skipped_todo = []
        self.finish = 0

    #def run(self):
        #while not

class Todo:
    def __init__(self, station, arrival, max_queue, purchase):
        self.station = station
        self.arrival = arrival
        self.max_queue = max_queue
        self.purchase = purchase

def generate_customer(sleep_time, name, todo):
    a = 1
    while not stop.is_set():
        k = Customer(str(name) + str(a), tuple(todo))
        k.start()
        print(k)
        customer_lock.acquire()
        customer.append(k)
        customer_lock.release()
        a += 1
        time.sleep(1)

stop = Event()
customer = []
customer_lock = Lock()

if __name__ == "__main__":
    baker = Station("Backer", 10)
    butcher = Station("Metzger", 30)
    cheese = Station("Kasetheke", 60)
    checkout = Station("Kasse", 5)

    baker.start()
    butcher.start()
    cheese.start()
    checkout.start()

    customer_a = [Todo(0, 10, 10, 10), Todo(1, 30, 5, 10), Todo(2, 45, 3, 5),
                   Todo(3, 10, 30, 20)]
    customer_b = [Todo(1, 30, 2, 5), Todo(3, 30, 3, 20), Todo(0, 20, 3, 20)]

    generate_a = Thread(target = generate_customer, args = (200, "A", customer_a))
    generate_b = Thread(target = generate_customer, args = (60, "B", customer_b))

    generate_a.start()
    time.sleep(1)
    generate_b.start()

    stop.set()

    baker.stop.set()
    butcher.stop.set()
    cheese.stop.set()
    checkout.stop.set()





