# creating Person class
class Person:  # this takes four parameters
               # 1: Total population
               # 2: initial infected population
               # 3: immune
               # 4: dead
    def __init__(self, total_population, infected, immune, dead):
        self.total_population = total_population
        self.susceptible = total_population - infected - dead - immune
        self.infected = infected
        self.immune = immune
        self.dead = dead
