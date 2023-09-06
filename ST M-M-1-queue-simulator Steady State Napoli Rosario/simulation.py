from event import Event
from customer import Customer

class Simulation:
    def __init__(self):
        self.state = "free"
        self.clock = 0.0


        self.future_event = []
        self.event_history = []

        self.response_time = []
        self.response_index = 0

        self.waiting_time=[]

        self.queue_length = 0
        self.n_departure = 0
        
        self.total_times=[]
        self.queue_distribution={}
        self.queue_distribution[0] = [0, self.clock, 0]
        self.expected_queue_length=0

    #Funzione per ordinare gli eventi del calendario rispetto al tempo
    def event_sort(self):
        self.future_event = sorted(self.future_event, key=lambda event: event.time)

    #Istanzio oggetto Customer ed eseguo il suo metodoto "arrival" 
    def customer_arrival(self):
        customer = Customer(self)
        customer.customer_arrival()


    def customer_departure(self):
        customer = Customer(self)
        customer.customer_departure()


    def calculateWaitingTime(self,termination):
        arrivals = []
        departures = []
        for elements in self.event_history:
            if elements[1] == "arrival":
                arrivals.append(elements)
            else:
                departures.append(elements)
        self.waiting_time.append(0)
        for i in range(termination//2, termination-1):
            waiting = departures[i][0]-arrivals[i+1][0]
            if (waiting < 0):
                waiting = 0
            self.waiting_time.append(waiting)

    def calculateResponseTime(self, termination):
        arrivals = []
        departures = []
        for elements in self.event_history:
            if elements[1] == "arrival":
                arrivals.append(elements)
            else:
                departures.append(elements)
        self.waiting_time.append(0)
        for i in range( termination//2, termination-1):
            response = departures[i][0]-arrivals[i][0]
            if (response < 0):
                response = 0
            self.response_time.append(response)

    
    def getExpectedQueueLength(self, tn):
        summatory=0
        for element in self.queue_distribution:
            summatory=summatory+(element*self.queue_distribution[element][0]) 
        self.expected_queue_length=summatory/tn
        return self.expected_queue_length
        
    

        

