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
                time.sleep(serve / 120)
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
        self.state = 0
        self.finish = 0
        self.get_served = Event()
        self.count_customer = 0
        self.counter = 0


    def run(self):
        global baker_count
        global butcher_count
        global checkout_count
        global cheese_count

        global starter
        global ender
        global added

        starter = datetime.datetime.now()
        self.counter += 1
        while self.actual_todo is not None:
            if (self.state == 0):
                print(str(datetime.datetime.now()) + ": " + self.name + " is walking.")
                self.state = 0
                time.sleep(self.actual_todo.arrival / 120)
            self.state = 1
            info_station = self.actual_todo.station
            info_station.lock.acquire()
            print(str(datetime.datetime.now()) + ": " + self.name + " is arrived at " + str(info_station.name))
            if len(info_station.queue) > self.actual_todo.queue_length:
                info_station.lock.release()
                print(
                    str(datetime.datetime.now()) + ": " + self.name + " skipped the queue at " + str(info_station.name))
                self.state = 0
                self.skipped_todo()
                if (info_station.name == "Kasetheke"):
                    cheese_count += 1
                elif (info_station.name == "Kasse"):
                    checkout_count += 1
                elif (info_station.name == "Metzger"):
                    butcher_count += 1
                else:
                    baker_count += 1
                continue
            else:
                info_station.queue.append(self)
                info_station.get_arrived.set()
            print(str(datetime.datetime.now()) + ": " + self.name + " is waiting at " + str(info_station.name))
            info_station.lock.release()
            self.get_served.wait()
            self.get_served.clear()
            self.finished_todo()
        ender = datetime.datetime.now()
        ender = ender - starter
        added += ender.total_seconds()


    def finished_todo(self):
        self.state = 0
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
butcher_count = 0
cheese_count = 0
checkout_count = 0
baker_count = 0

time_f = 0
time_t = 0
time_s = 0
time_z = 0

starter = 0
ender = 0
added = 0

def generate_customer(sleep_time, name, todo):
    global customer_count
    global time_f
    global time_t
    global time_s
    global time_z
    a = 1

    while not get_stopped.is_set():
        customer_count += 1
        k = Customer(str(name) + str(a), tuple(todo))
        k.start()
        customer_lock.acquire()
        customer.append(k)
        customer_lock.release()
        a += 1
        time.sleep(sleep_time / 120)



if __name__ == "__main__":
    baker = Station("Backer", 10)
    butcher = Station("Metzger", 30)
    cheese = Station("Kasetheke", 60)
    checkout = Station("Kasse", 5)
    customer_a = [Todo2(baker, 10, 10, 10), Todo2(butcher, 30, 10, 5), Todo2(cheese, 45, 5, 3),
                  Todo2(checkout, 60, 20, 30)]
    customer_b = [Todo2(butcher, 30, 5, 2), Todo2(checkout, 30, 20, 3), Todo2(baker, 20, 20, 3)]
    generate_a = Thread(target=generate_customer, args=(200, "A", customer_a))
    generate_b = Thread(target=generate_customer, args=(60, "B", customer_b))

    baker.start()
    butcher.start()
    cheese.start()
    checkout.start()
    timer_start = datetime.datetime.now()
    generate_a.start()
    time.sleep(1 / 120)
    generate_b.start()
    time.sleep(1800 / 120)
    timer_end = datetime.datetime.now()
    get_stopped.set()

    generate_a.join()
    generate_b.join()

    for customer in customer:
        customer.join()

    expire = timer_end - timer_start
    average_seconds = time_z / customer_count
    check = added / customer_count
    print("Simulationsende: " + str(expire))
    print("Anzahl Kunden:  " + str(customer_count))
    print("Mittlere Einkaufsdauer:  " + str(check))

    butcher_drop = 100 / customer_count * butcher_count
    cheese_drop = 100 / customer_count * cheese_count
    checkout_drop = 100 / customer_count * checkout_count
    baker_drop = 100 / customer_count * baker_count
    full_purchase = customer_count - butcher_count
    print("Anzahl vollstandige Einkaufe: " + str(full_purchase))
    print("Drop percentage Backer: " + str(baker_drop))
    print("Drop percentage Metzger: " + str(butcher_drop))
    print("Drop percentage Kase: " + str(cheese_drop))
    print("Drop percentage Kasse: " + str(checkout_drop))

    baker.get_stopped.set()
    butcher.get_stopped.set()
    cheese.get_stopped.set()
    checkout.get_stopped.set()
