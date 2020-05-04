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
        self.queue = []
        self.working = False
        self.lock = Lock()
        self.get_stopped = Event()
        self.get_arrived = Event()
        self.get_served = Event()

    def run(self):
        while not self.get_stopped.is_set():

            # Wait for a customer
            # Timeout to detect if the kill flag has been set
            if self.get_arrived.wait(1) is not True:
                continue

            while len(self.queue) != 0:
                customer2 = self.queue.pop(0)
                serve = customer2.actual_todo.purchase * self.dauer
                print(str(datetime.datetime.now()) + ": " + self.name + " serving customer " + str(
                    customer2.name) + " for " + str(serve) + " sec")
                time.sleep(serve / 90)
                customer2.get_served.set()
            self.get_arrived.clear()
            print(str(datetime.datetime.now()) + ": " + self.name + " has finished customer " + str(customer2.name))
            customer2.state = 0
            self.get_stopped.is_set()


class Customer(Thread):
    def __init__(self, name, todo):
        Thread.__init__(self)
        self.name = name
        self.todo = list(todo)
        self.actual_todo = self.todo.pop(0)
        self.skip_todo = []
        # 0 = walking
        # 1 = at station
        self.state = 0
        self.finish = 0
        self.get_served = Event()
        self.count_customer = 0
        self.time_s = datetime.datetime.now()
        self.time_f = None
        self.counter = 0

    def run(self):
        self.counter += 1
        while self.actual_todo is not None:
            if (self.state == 0):
                print(str(datetime.datetime.now()) + ": " + self.name + " is walking.")
                self.state = 0
                time.sleep(self.actual_todo.arrival / 90)
            self.state = 1
            info_station = self.actual_todo.station
            info_station.lock.acquire()
            print(str(datetime.datetime.now()) + ": " + self.name + " is arrived at " + str(info_station.name))
            if len(info_station.queue) > self.actual_todo.queue_length:
                info_station.lock.release()
                self.skipped_todo()
                continue
            else:
                info_station.queue.append(self)
                info_station.get_arrived.set()
            print(str(datetime.datetime.now()) + ": " + self.name + " is waiting at " + str(info_station.name))
            info_station.lock.release()
            self.get_served.wait()
            self.get_served.clear()
            self.finished_todo()
        self.time_f = datetime.datetime.now()

    def finished_todo(self):
        if len(self.todo) == 0:
            self.actual_todo = None
        else:
            self.actual_todo = self.todo.pop(0)

    def skipped_todo(self):
        self.skip_todo.append(self.actual_todo)
        self.finished_todo()


class Todo2:
    def __init__(self, station, arrival, queue_length, purchase):
        self.station = station
        self.arrival = arrival
        self.queue_length = queue_length
        self.purchase = purchase


get_stopped = Event()
customer = []
customer_lock = Lock()
customer_count = 0


def generate_customer(sleep_time, name, todo):
    global customer_count
    a = 1
    customer_count += 1
    while not get_stopped.is_set():
        k = Customer(str(name) + str(a), tuple(todo))
        k.start()
        customer_lock.acquire()
        customer.append(k)
        customer_lock.release()
        a += 1
        time.sleep(sleep_time / 90)


if __name__ == "__main__":
    baker = Station("Backer", 5)
    butcher = Station("Metzger", 5)
    cheese = Station("Kasetheke", 5)
    checkout = Station("Kasse", 5)
    customer_a = [Todo2(baker, 1, 1, 1), Todo2(butcher, 3, 5, 1), Todo2(cheese, 1, 3, 1),
                  Todo2(checkout, 1, 1, 1)]
    customer_b = [Todo2(butcher, 1, 2, 1), Todo2(checkout, 1, 3, 1), Todo2(baker, 1, 3, 1)]
    generate_a = Thread(target=generate_customer, args=(200, "A", customer_a))
    generate_b = Thread(target=generate_customer, args=(60, "B", customer_b))

    baker.start()
    butcher.start()
    cheese.start()
    checkout.start()
    timer_start = datetime.datetime.now()
    generate_a.start()
    time.sleep(1)
    generate_b.start()
    time.sleep(10)
    timer_end = datetime.datetime.now()
    get_stopped.set()

    expire = timer_end - timer_start
    print("Simulationsende: " + str(expire))
    print("Anzahl Kunden:  " + str(customer_count))

    generate_a.join()
    generate_b.join()

    for c in customer:
        c.join()

    baker.get_stopped.set()
    butcher.get_stopped.set()
    cheese.get_stopped.set()
    checkout.get_stopped.set()
