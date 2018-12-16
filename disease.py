from person import *
from random import *


# creating class of disease
class Disease:  # it takes two parameters
                # 1: possible days that a person stays infected by the disease
                # 2: average contact number during infection period
    def __init__(self, days_infected, contact_number):
        self.days_infected = days_infected

        # The rate of how quickly recovers
        self.infection_rate = 1 / self.days_infected

        # daily contact rate per infective person
        self.dayly_contact = contact_number * self.infection_rate

    # new case of susceptible tomorrow
    def new_case_susceptible(self, p_class):
        p_class.susceptible = (self.dayly_contact * (p_class.susceptible / p_class.total_population) * p_class.infected)
        return p_class.susceptible

    # new case of infected tomorrow
    def new_case_infected(self, new_case_susceptible, p_class):
        p_class.infected = (self.dayly_contact * (new_case_susceptible / p_class.total_population) * p_class.infected) - (self.infection_rate * p_class.infected)
        return p_class.infected


