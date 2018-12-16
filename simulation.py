from person import *
from disease import *
from aluLib import *
from random import *
from csv import *

# Constants for drawing
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
BAR_HEIGHT = 80
BAR_Y_COORD = 300
LEGEND_SIZE = 30
LEGEND_OFFSET = 250
LEGEND_TEXT_OFFSET = 210


disease_name = input('What is the disease name:')
# total number of days for our simulation to run
target_duration = int(input('Input the total number of days to run simulation:'))
# Setting up the population(From person class)
population = Person(int(input('Input total population to run the simulation:')),
                    int(input('Number of initial population infected:')),
                    0, 0)
# setting up disease information(from disease class)
disease = Disease(int(input('Input an estimation of days one can say sick:')),
                  int(input('Input a contact number per infective:')))
# The rate of recovery
recovery_rate = float(input('What is the chance for infected person to recover by next day(use range 0 to 1 eg: 0.4):'))
original_population_size = population.total_population
immune_count = population.immune
infected_count = population.infected
deceased_count = population.dead
susceptible_count = population.susceptible
origin_infected = population.infected


# Keep track of how many days it's been
day_count = 0


# displaying visual summary of each population
def draw_status():
    clear()
    set_font_size(24)
    draw_text("Total population is: " + str(immune_count + infected_count + susceptible_count + deceased_count), 10, 30)

    draw_text("Simulation for " + disease_name + " has been running for " + str(day_count) + " days", 10, 75)

    # Figure out how large we should make each population
    susceptible_width = (susceptible_count / original_population_size) * WINDOW_WIDTH
    infected_width = (infected_count / original_population_size) * WINDOW_WIDTH
    immune_width = (immune_count / original_population_size) * WINDOW_WIDTH
    dead_width = (deceased_count / original_population_size) * WINDOW_WIDTH

    # Start with susceptible
    set_fill_color(0, 1, 0)
    # Draw the bar
    if susceptible_count != 0:
        draw_rectangle(0, BAR_Y_COORD, susceptible_width, BAR_HEIGHT)
    # Draw the legend:
    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 30, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Susceptible', WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 60)

    # Draw infected
    set_fill_color(1, 0, 0)
    if infected_count != 0:
        draw_rectangle(susceptible_width, BAR_Y_COORD, infected_width, BAR_HEIGHT)

    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 75, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Infected', WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 105)

    # Draw immune
    set_fill_color(0, 0, 1)
    if immune_count != 0:
        draw_rectangle(susceptible_width + infected_width, BAR_Y_COORD, immune_width, BAR_HEIGHT)

    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 120, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Immune', WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 150)

    # Draw diseased
    set_fill_color(0.2, 0.7, 0.7)
    if deceased_count != 0:
        draw_rectangle(susceptible_width + infected_width + immune_width, BAR_Y_COORD, dead_width, BAR_HEIGHT)

    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 165, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Dead', WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 195)


# updating the number of infected_count on a daily basis
def check_the_infected():
    global infected_count
    # calculating the number of new case of the infected_count per day
    population.infected = population.infected + disease.new_case_infected(population.infected, population)
    infected_count = round(population.infected)  # updating infected_count


# updating the number of susceptible_count on a daily basis
def check_the_susceptible():
    global susceptible_count
    # calculating the number of new case of the susceptible_count per day
    population.susceptible = population.susceptible - disease.new_case_susceptible(population)
    susceptible_count = round(population.susceptible) # updating susceptible_count


# this function checks deceased or immune people on a daily basis
# it proves both numbers on a daily basis
def check_diseased_or_immune():
    global deceased_count, immune_count
    daily_immune = 0
    daily_deceased = 0
    # removed_population: is number of people who are not in susceptible and are not infected
    removed_population = original_population_size - (susceptible_count + infected_count)

    # checking each person in removed_population
    # whether the person recovers or is diseased
    for x in range(removed_population):
        if random() <= recovery_rate:
            daily_deceased += 1
        elif recovery_rate == 0:
            deceased_count = 0
        else:
            daily_immune += 1
    # updating deceased_count and immune_count
    deceased_count = daily_deceased
    immune_count = daily_immune


# writing a header of csv file
with open("simulation_report.csv", "a") as f:
    f.write("total_population,susceptible,infected,immune,deceased" + '\n')


# writing csv file report
def write_csv():
    with open("simulation_report.csv", "a") as csv_file:
        csv_file.write(str(original_population_size) + ',' + str(susceptible_count)+','+str(infected_count)+','+str(immune_count)+','+str(deceased_count) + "\n")


def generate_final_report():
    # percentage of the population survived?
    print('survival percent: ' + str(((susceptible_count + immune_count)/original_population_size) * 100))

    # calculating R0?
    r0 = ((infected_count + deceased_count)/origin_infected)/origin_infected
    print('Ro:' + str(r0))

    # checking whether we suffered epidemic or not
    if r0 >= 1:
        print('This is an epidemic')
    else:
        print('This not epidemic')


def main():
    global day_count
    # Draws the visual representation
    draw_status()

    # Loop over the infected population to determine if they could recover or pass away
    check_the_infected()

    # Loop over the healthy population to determine if they can catch the disease
    check_the_susceptible()

    check_diseased_or_immune()

    # Update our output CSV
    write_csv()

    day_count += 1

    # End the simulation once we reach the set target.
    if day_count == target_duration:
        generate_final_report()
        cs1_quit()


start_graphics(main, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, framerate=1)
