from threading import Thread
import time
from threading import Event
from threading import Lock
import datetime


class Task:
    def __init__(self, station, arrival_time, max_queue_length, amount):
        self.station = station
        self.arrival_time = arrival_time
        self.max_queue_length = max_queue_length
        self.amount = amount

class Station(Thread):
    def __init__(self, name, duration):
        Thread.__init__(self)
        self.name = name
        self.duration = duration
        self.queue = []
        self.is_busy = False
        self.arrEv = Event()
        self.servEv = Event()
        self.killEv = Event()
        self.lock = Lock()
        self.FACTOR = 10

    def run(self):
        # Loop until kill flag is set
        while not self.killEv.is_set():

            # Wait for a customer
            # Timeout to detect if the kill flag has been set
            if self.arrEv.wait(10) is not True:
                continue

            self.is_busy = True
            while len(self.queue) != 0:
                customer = self.queue.pop(0)
                serving_time = customer.current_task.amount * self.duration
                print(f"{self.name} serving customer {customer} for {serving_time} sec.")
                time.sleep(serving_time // self.FACTOR)
                customer.servEv.set()
            self.is_busy = False
            self.arrEv.clear()


class Customer(Thread):
    def __init__(self, name, tasks):
        Thread.__init__(self)
        self.tasks = list(tasks)
        self.name = name
        self.current_task = self.tasks.pop(0)
        self.skipped_tasks = []
        self.servEv = Event()
        self.FACTOR = 10
        self.start_time = datetime.datetime.now()
        self.finish_time = None

    def run(self):
        print(f"{self.name} {self.start_time.strftime('%X')} is running.")
        while self.current_task is not None:
            time.sleep(self.current_task.arrival_time // self.FACTOR)
            s = self.current_task.station
            s.lock.acquire()
            if s.is_busy and len(s.queue) > self.current_task.max_queue_length:
                self.skip_current_task()
                s.lock.release()
                continue
            else:
                s.queue.append(self)
                s.arrEv.set()
            s.lock.release()
            print(f"{self.name} is waiting at {s}.")
            self.servEv.wait()
            self.servEv.clear()
            self.finish_current_task()
        self.finish_time = datetime.datetime.now()
        print(f"{self.name} {self.finish_time.strftime('%X')} has finished.")

    def finish_current_task(self):
        if len(self.tasks) == 0:
            self.current_task = None
        else:
            self.current_task = self.tasks.pop(0)

    def skip_current_task(self):
        self.skipped_tasks.append(self.current_task)
        self.finish_current_task()


killEv = Event()
customers = []
customers_lock = Lock()


def start_customers(sleep_time, name, tasks):
    a = 1
    while not killEv.is_set():
        k = Customer(f"{name}{a}", tuple(tasks))
        k.start()
        a += 1
        customers_lock.acquire()
        customers.append(k)
        customers_lock.release()
        time.sleep(sleep_time // 10)


if __name__ == "__main__":
    baecker = Station("Bäcker", 10)
    wursttheke = Station("Metzger", 30)
    kaesetheke = Station("Käsetheke", 60)
    kasse = Station("Kasse", 5)

    baecker.start()
    wursttheke.start()
    kaesetheke.start()
    kasse.start()

    tasks_type1 = [Task(baecker, 10, 10, 10), Task(wursttheke, 30, 5, 10), Task(kaesetheke, 45, 3, 5),
                   Task(kasse, 10, 30, 20)]
    tasks_type2 = [Task(wursttheke, 30, 2, 5), Task(kasse, 30, 3, 20), Task(baecker, 20, 3, 20)]

    starter_type1 = Thread(target=start_customers, args=(200, "A", tasks_type1))
    starter_type2 = Thread(target=start_customers, args=(60, "B", tasks_type2))

    simulation_start = datetime.datetime.now()
    starter_type1.start()
    time.sleep(1//10)
    starter_type2.start()
    time.sleep(100 // 10)
    killEv.set()

    starter_type1.join()
    starter_type2.join()

    for k in customers:
        k.join()

    simulation_end = datetime.datetime.now()




    # Calculate simulation results
    print(f"Simulationsende: {(simulation_end - simulation_start).total_seconds()}s")
    print(f"\n\nAnzahl Kunden: {len(customers)}")
    vollständige_einkäufe = len(list(filter(lambda kunde: len(kunde.skipped_tasks) == 0, customers)))
    print(f"Anzahl vollständige Einkäufe: {vollständige_einkäufe}")

    average_shopping_time = 0
    for k in customers:
        average_shopping_time += (k.finish_time - k.start_time).total_seconds()
    average_shopping_time /= len(customers)
    print(f"Mittlere Einkaufsdauer: {average_shopping_time}s")

    average_shopping_time_completed = 0
    for k in list(filter(lambda e: len(e.skipped_tasks) == 0, customers)):
        average_shopping_time_completed += (k.finish_time - k.start_time).total_seconds()
    average_shopping_time_completed /= len(customers)
    print(f"Mittlere Einkaufsdauer (vollständig): {average_shopping_time_completed}s")

    all_skipped_stations = []
    for x in customers:
        skipped_stations = list(map(lambda e: e.station, x.skipped_tasks))
        all_skipped_stations.extend(skipped_stations)

    dropped_at_Bäcker = len(list(filter(lambda e: e.name == "Bäcker", all_skipped_stations)))
    dropped_at_Wursttheke = len(list(filter(lambda e: e.name == "Wursttheke", all_skipped_stations)))
    dropped_at_Käsetheke = len(list(filter(lambda e: e.name == "Käsetheke", all_skipped_stations)))
    dropped_at_Kasse = len(list(filter(lambda e: e.name == "Kasse", all_skipped_stations)))

    if len(all_skipped_stations) > 0:
        print(f"Drop percentage at Bäcker: {dropped_at_Bäcker / len(all_skipped_stations)}")
        print(f"Drop percentage at Wursttheke: {dropped_at_Wursttheke / len(all_skipped_stations)}")
        print(f"Drop percentage at Käsetheke: {dropped_at_Käsetheke / len(all_skipped_stations)}")
        print(f"Drop percentage at Kasse: {dropped_at_Kasse / len(all_skipped_stations)}")

    # Kill the stations
    baecker.killEv.set()
    wursttheke.killEv.set()
    kaesetheke.killEv.set()
    kasse.killEv.set()