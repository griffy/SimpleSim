"""
A demonstration of what can be done with SimpleSim

Runs a simulation of the front counter of a restaurant, 
which is a single-server system (M/G/1) in this case

Customers arrive in groups according to the Poisson process at a 
specified rate (lambda) and pay for their meal first

The amount of customers in a group is according to the uniform
distribution from 1 to 6 inclusive

Service time is according to a custom distribution
"""
from collections import deque

from simplesim import rand
from simplesim.model import Model
from simplesim.event import Event

# let's arbitrarily decide to make our sim use a minutes-based clock
ONE_DAY = 60 * 24

# a service time of 2 minutes has a 55% chance of happening, and so on
service_time = rand.generator({
    2: 0.55,
    3: 0.30,
    4: 0.10,
    5: 0.05
})

class CustomerArriveCounterEvent(Event):
    def __init__(self, time):
        Event.__init__(self, time)
        self.customer_count = rand.uniform(1, 6)

class CustomerDepartCounterEvent(Event): pass

class RestaurantModel(Model):
    def initialize(self):
        """ initialize is called at the beginning of each run """
        self.counter_queue = deque([])
        # we schedule our first event here to get the ball rolling
        first_event = CustomerArriveCounterEvent(0)
        self.schedule_event(first_event)

    def update(self):
        pass

    def handle(self, event):
        if isinstance(event, CustomerArriveCounterEvent):
            # Stats objects are special - you can create their attributes
            # on-the-fly and assign values to them iteratively. Each
            # assignment will be remembered in a list so that you can
            # later ask for the mean, stdev, etc.
            self.stats.num_customers = event.customer_count
            # add them to the queue at the counter
            cur_time = self.clock.time()
            self.counter_queue.append((cur_time, event.customer_count))
            if len(self.counter_queue) == 1:
                # update wait time for customer in queue
                queue_time, _ = self.counter_queue[0]
                self.stats.wait_time = cur_time - queue_time
                # schedule their departure from the counter
                # based on the service time
                serv_time = service_time()
                self.stats.service_time = serv_time
                depart_time = cur_time + serv_time
                depart_event = CustomerDepartCounterEvent(depart_time)
                self.schedule_event(depart_event)
            # lambda = 1/5, ie 1 person every 5 minutes, or perhaps
            # a better way of stating it, since our sim is in terms
            # of minutes, is 1/5 of a person per minute
            next_arrival_time = cur_time + rand.exponential(1.0/5)
            next_event = CustomerArriveCounterEvent(next_arrival_time)
            self.schedule_event(next_event)
        elif isinstance(event, CustomerDepartCounterEvent):
            # remove the group of customers from the queue now
            _, count = self.counter_queue.popleft()
            # mark how many were served in that bunch
            self.stats.num_served = count 
            cur_time = self.clock.time()
            if len(self.counter_queue) > 0:
                # update wait time for next customer in queue
                queue_time, _ = self.counter_queue[0]
                self.stats.wait_time = cur_time - queue_time
                # schedule the next customer departure from the counter
                serv_time = service_time()
                self.stats.service_time = serv_time
                depart_time = self.clock.time() + serv_time
                depart_event = CustomerDepartCounterEvent(depart_time)
                self.schedule_event(depart_event)

model = RestaurantModel()
stats = model.run(1000, ONE_DAY, seed=0xDEADBEEF)
print stats
