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
        # init counter for calculations for the statistics
        self.count_customer_baker = 0
        self.count_customer_butcher = 0
        self.count_customer_cheese = 0
        self.count_customer_checkout = 0
        self.drop_customer_baker = 0
        self.drop_customer_butcher = 0
        self.drop_customer_cheese = 0
        self.drop_customer_checkout = 0
        self.count_A = 0
        self.count_B = 0
        self.spawn_times = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 0, 61, 121, 181, 241, 301, 361, 421,
                            481, 541, 601, 661, 721, 781, 841, 901, 961, 1021, 1081, 1141, 1201, 1261, 1321, 1381, 1441,
                            1501, 1561, 1621, 1681, 1741, 1801, 1861, 1921, 1981, 2041]
        self.go_counter = 0
        self.add_average_counter = 0
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
            if (customer_typ == "A"):
                self.count_A = self.count_A + 1
            elif (customer_typ == "B"):
                self.count_B += 1

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
                        self.count_customer_baker += 1
                    elif store_location == 1:
                        self.arrive(timeFromStart, store_location, customer, self.butcher)
                        self.count_customer_butcher += 1
                    elif store_location == 2:
                        self.arrive(timeFromStart, store_location, customer, self.cheese)
                        self.count_customer_cheese += 1
                    else:
                        self.arrive(timeFromStart, store_location, customer, self.checkout)
                        self.count_customer_checkout += 1
                # purchase order for customer type B
                else:
                    if store_location == 0:
                        self.arrive(timeFromStart, store_location, customer, self.butcher)
                        self.count_customer_butcher += 1
                    elif store_location == 1:
                        self.arrive(timeFromStart, store_location, customer, self.checkout)
                        self.count_customer_checkout += 1
                    else:
                        self.arrive(timeFromStart, store_location, customer, self.baker)
                        self.count_customer_baker += 1
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
                        self.add_average_counter = self.add_average_counter + (timeFromStart - self.spawn_times[self.go_counter])
                        self.go_counter += 1

                # purchase order for customer type B
                else:
                    if store_location == 0:
                        self.leave(timeFromStart, store_location, customer, self.butcher)
                    elif store_location == 1:
                        self.leave(timeFromStart, store_location, customer, self.checkout)
                        self.add_average_counter = self.add_average_counter + (timeFromStart - self.spawn_times[self.go_counter])
                        self.go_counter += 1
                    else:
                        self.leave(timeFromStart, store_location, customer, self.baker)
        count_C = self.count_A + self.count_B
        print("Simulationsende: " + str(timeFromStart) + "s")
        print("Anzahl Kunden: " + str(count_C))
        percentage_butcher = 100 / self.count_customer_butcher * self.drop_customer_butcher
        percentage_baker = 100 / self.count_customer_baker * self.drop_customer_baker
        percentage_cheese = 100 / self.count_customer_cheese * self.drop_customer_cheese
        percentage_checkout = 100 / self.count_customer_checkout * self.drop_customer_checkout
        all_skipped = count_C - (self.drop_customer_butcher + self.drop_customer_baker + self.drop_customer_cheese + self.drop_customer_checkout)
        average = self.add_average_counter / count_C
        print("Mittlere Einkaufsdauer: " + str(average))
        print("Anzahl vollständige Einkäufe: " + str(all_skipped))
        print("Drop percentage at Bäcker: " + str(percentage_baker))
        print("Drop percentage at Metzger: " + str(percentage_butcher))
        print("Drop percentage at Käse: " + str(percentage_cheese))
        print("Drop percentage at Kasse: " + str(percentage_checkout))
        station_file = open("supermarkt.txt", "a")
        station_file.write("Simulationsende: " + str(timeFromStart) + "s\n")
        station_file.write("Anzahl Kunden: " + str(count_C) + "\n")
        station_file.write("Mittlere Einkaufsdauer: " + str(average) + "\n")
        station_file.write("Anzahl vollständige Einkäufe: " + str(all_skipped) + "\n")
        station_file.write("Drop percentage at Bäcker: " + str(percentage_baker) + "\n")
        station_file.write("Drop percentage at Metzger: " + str(percentage_butcher) + "\n")
        station_file.write("Drop percentage at Käse: " + str(percentage_cheese) + "\n")
        station_file.write("Drop percentage at Kasse: " + str(percentage_checkout) + "\n")
        station_file.close()

    # if customer arrives at store
    def arrive(self, timeFromStart, store_location, customer, station):
        # if user is skipping queue, because its to long
        if len(station.queue) >= customer.taskOrder[store_location][1]:
            if store_location < len(customer.taskOrder) - 1:
                self.push((timeFromStart + customer.taskOrder[store_location + 1][0], 2, 'A' + str(store_location + 1), customer))
                customer.save(timeFromStart, 'Skipping', station)
                if (station.name == "Baecker"):
                    self.drop_customer_baker += 1
                elif (station.name == "Metzger"):
                    self.drop_customer_butcher += 1
                elif (station.name == "Käse"):
                    self.drop_customer_cheese += 1
                elif (station.name == "Kasse"):
                    self.drop_customer_checkout += 1


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
            self.push((timeFromStart + queue_customer.taskOrder[store][2] * station.workTime, 1, 'C' + str(store),queue_customer))
        # if there are no customers waiting for this store
        else:
            station.working = False

    def finish(self, kunde):
        print(kunde)


# starting the shopping event
if __name__ == "__main__":
    start_store = eventOriented(2000, 100000)
    start_store.open()
