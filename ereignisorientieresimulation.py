import heapq

# define store attributes
class Store:
    # init store
    def __init__(self, name, workTime):
        self.name = name
        self.workTime = workTime
        self.queue = list()
        self.working = False
    # write in station file who get served at which time on which store
    def save(self, timeFromStart, activity, customer):
        station_file = open("supermarkt_station.txt", "a")
        station_file.write(str(timeFromStart) + ':' + self.name + ' ' + activity + ' customer ' + customer.name + '\n')
        station_file.close()

# define customer attributes
class Customer:
    def __init__(self, name):
        self.name = name
        # init tasks for type A
        if name[0] == "A":
            self.taskOrder = list([(10, 10, 10), (30, 10, 5), (45, 5, 3), (60, 20, 30)])
        # init tasks for type B
        elif name[0] == "B":
            self.taskOrder = list([(30, 5, 2), (30, 20, 3), (20, 20, 3)])

    # write in customer file what happens at which time
    def save(self, timeFromStart, activity, station):
        customer_file = open("supermarkt_customer.txt", "a")
        customer_file.write(str(timeFromStart) + ':' + self.name + ' ' + activity + ' at ' + station.name + '\n')
        customer_file.close()

    def __lt__(self, nott):
        return self.name < nott.name


class eventOriented:
    def __init__(self, timeFromStart, eventnumber):
        # init heap
        self.heapq = []
        # init time
        self.timeFromStart = timeFromStart
        self.number = eventnumber
        # init customer respawn
        self.generateCustomer(0, 200, self.timeFromStart, "A")
        self.generateCustomer(1, 60, self.timeFromStart, "B")
        # init stores
        self.baker = Store('Baecker', 10)
        self.butcher = Store('Metzger', 30)
        self.cheese = Store('Käse', 60)
        self.checkout = Store('Kasse', 5)

    # pop from heap
    def pop(self):
        return heapq.heappop(self.heapq)

    # push from heap
    def push(self, event):
        heapq.heappush(self.heapq, event)

    # Generate new customer
    def generateCustomer(self, startTime, recurringTime, timeFromStart, customer_typ):
        timer = startTime
        customerId = 1
        # generating respawn time and customerid
        while timer < timeFromStart:
            self.push((timer, 0, 'B', Customer(customer_typ + str(customerId))))
            timer += recurringTime
            customerId += 1

    def open(self):
        time = 0
        eventnumber = 0
        while self.heapq or time >= self.timeFromStart or eventnumber >= self.number:
            timeFromStart, prio, event, customer = self.pop()
            # start the store
            if event == 'B':
                self.push((timeFromStart + customer.taskOrder[0][0], 2, 'A0', customer))
            # if customer is ready to queue
            elif event[0] == 'A':
                store_location = int(event[1])
                # purchase order for customer type A
                if customer.name[0] == 'A':
                    if store_location == 0:
                        self.arrive(timeFromStart, store_location, customer, self.baker)
                    elif store_location == 1:
                        self.arrive(timeFromStart, store_location, customer, self.butcher)
                    elif store_location == 2:
                        self.arrive(timeFromStart, store_location, customer, self.cheese)
                    else:
                        self.arrive(timeFromStart, store_location, customer, self.checkout)
                # purchase order for customer type B
                else:
                    if store_location == 0:
                        self.arrive(timeFromStart, store_location, customer, self.butcher)
                    elif store_location == 1:
                        self.arrive(timeFromStart, store_location, customer, self.checkout)
                    else:
                        self.arrive(timeFromStart, store_location, customer, self.baker)
            # if customer is ready to leave
            elif event[0] == 'C':
                # purchase order for customer type A
                store_location = int(event[1])
                if customer.name[0] == 'A':
                    if store_location == 0:
                        self.leave(timeFromStart, store_location, customer, self.baker)
                    elif store_location == 1:
                        self.leave(timeFromStart, store_location, customer, self.butcher)
                    elif store_location == 2:
                        self.leave(timeFromStart, store_location, customer, self.cheese)
                    else:
                        self.leave(timeFromStart, store_location, customer, self.checkout)
                # purchase order for customer type B
                else:
                    if store_location == 0:
                        self.leave(timeFromStart, store_location, customer, self.butcher)
                    elif store_location == 1:
                        self.leave(timeFromStart, store_location, customer, self.checkout)
                    else:
                        self.leave(timeFromStart, store_location, customer, self.baker)

    # if customer arrives at store
    def arrive(self, timeFromStart, store_location, customer, station):
        # if user is skipping queue, because its to long
        if len(station.queue) >= customer.taskOrder[store_location][1]:
            if store_location < len(customer.taskOrder) - 1:
                self.push((timeFromStart + customer.taskOrder[store_location + 1][0], 2, 'A' + str(store_location + 1), customer))
                customer.save(timeFromStart, 'Skipping', station)
        # user wants to get to store
        else:
            # write to txt
            station.save(timeFromStart, 'adding', customer)
            station.queue.append((customer, store_location))
            # if their is no queue
            if not station.working:
                station.save(timeFromStart, 'serving', customer)
                station.working = True
                station.queue.pop(0)
                customer.save(timeFromStart, 'Queueing', station)
                self.push((timeFromStart + station.workTime * customer.taskOrder[store_location][2], 1, 'C' + str(store_location), customer))
            # if there is a queue
            else:
                customer.save(timeFromStart, 'Queueing', station)

    # customer leaves at store
    def leave(self, timeFromStart, store_location, customer, station):
        # write to txt
        customer.save(timeFromStart, 'Finished', station)
        station.save(timeFromStart, 'finished', customer)
        # if store is in range
        if store_location < len(customer.taskOrder) - 1:
            self.push((timeFromStart + customer.taskOrder[store_location + 1][0], 2, 'A' + str(store_location + 1), customer))
        # if customer are waiting for this store
        if station.queue:
            queue_customer, store = station.queue.pop(0)
            station.save(timeFromStart, 'serving', queue_customer)
            self.push((timeFromStart + queue_customer.taskOrder[store][2] * station.workTime, 1,'C' + str(store), queue_customer))
        # if there are no customers waiting for this store
        else:
            station.working = False

# starting the shopping event
if __name__ == "__main__":
    start_store = eventOriented(2000, 100000)
    start_store.open()
