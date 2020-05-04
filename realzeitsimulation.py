from threading import Thread
from _thread import start_new_thread
import time
from threading import Event
from threading import Lock
import datetime

"""class Store(Thread):
    def __init__(self, name, dauer):
        self.name = name
        self.dauer = dauer

    def run(self):
        while not"""

class Customer(Thread):
    def __init__(self, name, todo):
        Thread.__init__(self)
        self.name = name
        self.todo = list(todo)
        self.actual_todo = self.todo.pop(0)
        self.skipped_todo = []
        self.start = datetime.datetime.now()
        self.finish = 0

    def run(self):
        while not

class Todo:
    def __init__(self, station, arrival, max_queue, purchase):
        self.station = station
        self.arrival = arrival
        self.max_queue = max_queue
        self.purchase = purchase

if __name__ == "__main__":
    """baker = Store("Backer", 10)
    butcher = Store("Metzger", 30)
    cheese = Store("Kasetheke", 60)
    checkout = Store("Kasse", 5)"""

    customer_a = [Todo(0, 10, 10, 10), Todo(1, 30, 5, 10), Todo(2, 45, 3, 5),
                   Todo(3, 10, 30, 20)]
    customer_b = [Todo(1, 30, 2, 5), Todo(3, 30, 3, 20), Todo(0, 20, 3, 20)]

    generate_a = Thread(target=generate_customer, args=(200, "A", customer_a))
    generate_b = Thread(target=generate_customer, args=(60, "B", customer_b))

    generate_a.start()
    generate_b.start()

    """baker.start()
    butcher.start()
    cheese.start()
    checkout.start()"""


    """start_new_thread(baker)
    start_new_thread(butcher)
    start_new_thread(cheese)
    start_new_thread(checkout)"""

def baker1():
    print("baker is sleeping")
    time.sleep(300)
    print("baker woke up")
t = Thread(target = baker1)
t.start()



