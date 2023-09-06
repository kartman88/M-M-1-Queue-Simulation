import numpy as np
from event import Event


arrival_rate = 2.0
departure_rate=2.5 

class Customer:
    id_counter = 0

    def __init__(self, simulation):
        Customer.id_counter += 1
        self.id = Customer.id_counter
        self.simulation = simulation

    def customer_arrival(self):
        #crea evento arrivo nel calendario al tempo t (quello corrente) + fattore randomico
        self.simulation.future_event.append(Event("arrival", self.simulation.clock + np.random.exponential(1/arrival_rate))) #esponenziale perchè si riferisce tempo trascorso tra due eventi indipendenti (memoryless)
        
        #caso in cui nessuno usa la risorsa
        if self.simulation.state == "free":
            self.simulation.state = "busy" #cambiamo lo stato ad occupato se prima dell'arrival era libero
            self.simulation.future_event.append(Event("departure", self.simulation.clock + np.random.exponential(1/departure_rate))) #schedulo la sua departure
        else:
            #accodiamo il customer alla coda
            self.simulation.queue_length += 1

            #Aggiornamento distribuzione

            if  not self.simulation.queue_distribution.get(self.simulation.queue_length):
                self.simulation.queue_distribution[self.simulation.queue_length] = [0, self.simulation.clock, 0]
            else:
                self.simulation.queue_distribution[self.simulation.queue_length][1] = self.simulation.clock
                
            self.simulation.queue_distribution[self.simulation.queue_length-1][2] =self.simulation.clock
            self.simulation.queue_distribution[self.simulation.queue_length-1][0] += self.simulation.clock - self.simulation.queue_distribution[self.simulation.queue_length-1][1]
        
        #riordiniamo il calendario degli eventi
        self.simulation.event_sort()
        #inseriamo l'evento nella storia degli eventi accaduti
        self.simulation.event_history.append((self.simulation.clock, "arrival"))



    def customer_departure(self):
        self.simulation.state = "free" #setta lo stato del servizio a free
        self.simulation.n_departure += 1 #aumentiamo il numero di departure
        #waiting index indica il customer

        #se dopo la departure ci sono custoemr
        if self.simulation.queue_length != 0:
            self.simulation.queue_length -= 1

            #Aggiornamento distribuzione
            self.simulation.queue_distribution[self.simulation.queue_length][1] = self.simulation.clock
            self.simulation.queue_distribution[self.simulation.queue_length+1][2] = self.simulation.clock
            self.simulation.queue_distribution[self.simulation.queue_length+1][0] += self.simulation.queue_distribution[self.simulation.queue_length +1][2]-self.simulation.queue_distribution[self.simulation.queue_length+1][1]
           
           #cambio stato
            self.simulation.state = "busy" #prendiamo il nuovo, cambiamo lo stato e scheduliamo la departure
            departure_time = self.simulation.clock + np.random.exponential(1/departure_rate)
            self.simulation.future_event.append(Event("departure", departure_time))
            self.simulation.event_sort()
        self.simulation.event_history.append((self.simulation.clock, "departed"))
