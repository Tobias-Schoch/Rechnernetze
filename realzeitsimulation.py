from threading import Thread
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
        self.queue = []
        self.working = False

    #def run(self):
        #while


class Customer(Thread):
    def __init__(self, name, todo):
        Thread.__init__(self)
        self.name = name
        self.todo = list(todo)
        self.actual_todo = self.todo.pop(0)
        self.skipped_todo = []
        # 0 = walking
        # 1 = at station
        self.state = 0
        self.finish = 0

    def run(self):
        print(self.name + " is walking.")
        time.sleep(self.actual_todo.arrival / 20)
        while self.state == 0:
            print(self.name + " is arrived")

            station = self.actual_todo.station
            if len(station.queue) > self.actual_todo.queue_length:
                continue
            print(self.name + " is waiting at " + str(station))




class Todo:
    def __init__(self, station, arrival, queue_length, purchase):
        self.station = station
        self.arrival = arrival
        self.queue_length = queue_length
        self.purchase = purchase


def generate_customer(sleep_time, name, todo):
    a = 1
    while not stop.is_set():
        k = Customer(str(name) + str(a), tuple(todo))
        k.start()
        customer_lock.acquire()
        customer.append(k)
        customer_lock.release()
        a += 1
        time.sleep(sleep_time)


stop = Event()
customer = []
customer_lock = Lock()

if __name__ == "__main__":
    baker = Station("Backer", 10)
    butcher = Station("Metzger", 30)
    cheese = Station("Kasetheke", 60)
    checkout = Station("Kasse", 5)
    customer_a = [Todo(0, 10, 10, 10), Todo(1, 30, 5, 10), Todo(2, 45, 3, 5), Todo(3, 10, 30, 20)]
    customer_b = [Todo(1, 30, 2, 5), Todo(3, 30, 3, 20), Todo(0, 20, 3, 20)]
    generate_a = Thread(target=generate_customer, args=(200, "A", customer_a))
    generate_b = Thread(target=generate_customer, args=(60, "B", customer_b))

    baker.start()
    butcher.start()
    cheese.start()
    checkout.start()
    generate_a.start()
    time.sleep(1)
    generate_b.start()
    time.sleep(60)

    stop.set()
    baker.stop.set()
    butcher.stop.set()
    cheese.stop.set()
    checkout.stop.set()
