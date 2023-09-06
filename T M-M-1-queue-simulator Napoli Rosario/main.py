from simulation import Simulation
from event import Event
from tabulate import tabulate
import matplotlib.pyplot as plt
import scipy.stats as stats

from customer import arrival_rate, departure_rate
confidence_level = 0.95

#arrival rate less than service rate



if __name__ == "__main__":
    simulation_number = 100
    terminating_condition=2000
    waiting_time_list = [] #lista che contiene tutte le medie dei waiting delle simulazioni singole
    response_time_list = [] #lista che contiene tutte le medie dei response delle simulazioni singole
    utilizations_list = [] #lista che contiene tutte le medie di utilization delle singole simulazioni
    expected_queue_lengths=[] #lista che contiene tutte le medie di expected_queue_length delle singole simulazioni    

    
    for i in range(simulation_number): 
        free_time = 0
        state_change = False  
        old_clock = 0 #serve per free time 
        waiting_time=[]
        sim = Simulation() #inizializzo simulazione
        sim.future_event.append(Event("arrival", 0)) #schedulo un arrival

        while (sim.n_departure < terminating_condition): #condizione di terminazione della simulazione
            new_event = sim.future_event.pop(0) #prelevo l'evento dalla event list
            sim.clock = new_event.time #aggiorniamo il clock di sistema all'evento preso
            if new_event.type == "arrival":
                sim.customer_arrival() #creazione oggetto customer
            else:
                sim.customer_departure()
            #sezione per il free time
            if sim.state == "free": #quando non ci sono customer che si stanno servendo e la coda è vuota  mi segno il tempo in cui il server non lavora
                old_clock = sim.clock
                state_change = True
            elif state_change:
                free_time += sim.clock - old_clock #sommo il tempo in cui è stata vuota (state change passa a False appena c'è un arrival)
                state_change = False
            
        #Single Simulation Calculations
        #Utilization
        end_time = sim.clock
        utilization = 1 - (free_time / end_time)
        utilizations_list.append(utilization)

        #Response Time
        sim.calculateResponseTime(terminating_condition)
        average_response_time = sum(sim.response_time) / len(sim.response_time)
        response_time_list.append(average_response_time)

        #Expected Queue Length
        sim.getExpectedQueueLength(end_time-free_time)
        expected_queue_lengths.append(sim.expected_queue_length)
        event_history = sim.event_history  # Storico degli eventi """
        
        #Waiting Time
        sim.calculateWaitingTime(terminating_condition)
        average_waiting_time = sum(sim.waiting_time) / len(sim.waiting_time)
        waiting_time_list.append(average_waiting_time)


        # Calculate confidence intervals for utilization
        utilization_mean = sum(utilizations_list) / len(utilizations_list)
        utilization_std = stats.sem(utilizations_list)
        utilization_margin = utilization_std * stats.t.ppf((1 + confidence_level) / 2, len(utilizations_list) - 1)
        utilization_ci_lower = utilization_mean - utilization_margin
        utilization_ci_upper = utilization_mean + utilization_margin    

        # Calculate confidence intervals for expected waiting time
        response_time_mean = sum(response_time_list) / len(response_time_list)
        response_time_std = stats.sem(response_time_list)
        response_time_margin = response_time_std * stats.t.ppf((1 + confidence_level) / 2, len(waiting_time_list) - 1)
        response_time_ci_lower = response_time_mean - response_time_margin
        response_time_ci_upper = response_time_mean + response_time_margin

        # Calculate confidence intervals for expected queue length
        queue_length_mean = sum(expected_queue_lengths) / len(expected_queue_lengths)
        queue_length_std = stats.sem(expected_queue_lengths)
        queue_length_margin = queue_length_std * stats.t.ppf((1 + confidence_level) / 2, len(expected_queue_lengths) - 1)
        queue_length_ci_lower = queue_length_mean - queue_length_margin
        queue_length_ci_upper = queue_length_mean + queue_length_margin

        # Calculate confidence intervals for expected waiting time
        waiting_time_mean = sum(waiting_time_list) / len(waiting_time_list)
        waiting_time_std = stats.sem(waiting_time_list)
        waiting_time_margin = waiting_time_std * stats.t.ppf((1 + confidence_level) / 2, len(waiting_time_list) - 1)
        waiting_time_ci_lower = waiting_time_mean - waiting_time_margin
        waiting_time_ci_upper = waiting_time_mean + waiting_time_margin




        table = tabulate(event_history, headers=["Time", "Event"], floatfmt=".8f", tablefmt="fancy_grid")
        print("History Simulation", i+1, ":")
        print(table)
        
        #Calcoli Teorici 
        ro=arrival_rate/departure_rate

        theoretical_expected_queue_length=ro/(1-ro)
        theoretical_response_time=1/(departure_rate-arrival_rate)
        theoretical_utilization=ro



        def plot_measures(measure, xlabel, ylabel, title, ci_lower, ci_upper, little_law_value=0):
            plt.plot(measure)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            plt.axhline(sum(measure)/len(measure), color='r', linestyle='--', label='Average Value')
            plt.axhline(ci_lower, color='g', linestyle=':', label='CI Lower Bound')
            plt.axhline(ci_upper, color='y', linestyle=':', label='CI Upper Bound')
            if little_law_value!=0:
                plt.axhline(y=little_law_value, color='purple', linestyle='dashed', linewidth=1, label="Theoretical Value")
            plt.legend()
            plt.show()



    # Response Times Final Result
    plot_measures(response_time_list, "Simulations", "Response Time", "Response Time during Simulations",response_time_ci_lower, response_time_ci_upper,theoretical_response_time)

    # Expected Queue Length Final Result
    plot_measures(expected_queue_lengths, "Simulations", "Expected Queue Length","Expected Queue Length during Simulations",queue_length_ci_lower, queue_length_ci_upper,theoretical_expected_queue_length)

    # Utilization Final Result
    plot_measures(utilizations_list, "Simulations", "Utilization", "Utilization during Simulations",utilization_ci_lower, utilization_ci_upper, theoretical_utilization)

    # Waiting Times Final Result
    plot_measures(waiting_time_list, "Simulations", "Waiting Time", "Waiting Time during Simulations", waiting_time_ci_lower, waiting_time_ci_upper)

    

  
    
    
