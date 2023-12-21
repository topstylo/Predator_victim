"""This module will contain functions for deleting file"""
import os


def write_data(list_victim, list_predator, time):
    """ Function add line in data.txt file

    Parameters
    ----------
    list_predator : list
        list of predators
    list_victim : list
        list of victims
    time : int
        current time = step of modelling

    Returns
    ----------
    """

    list_victim_age = [cell.age for cell in list_victim]
    list_predator_age = [cell.age for cell in list_predator]

    list_victim_max_speed = [cell.max_speed for cell in list_victim]
    list_predator_max_speed = [cell.max_speed for cell in list_predator]

    list_victim_satiety = [cell.satiety * 100 for cell in list_victim]
    list_predator_satiety = [cell.satiety * 100 for cell in list_predator]

    number_of_victims = len(list_victim)
    number_of_predators = len(list_predator)

    victim_average_age = (sum(list_victim_age) / number_of_victims
                          if number_of_victims > 0 else 0)
    predator_average_age = (sum(list_predator_age) / number_of_predators
                            if number_of_predators > 0 else 0)

    victim_average_max_speed = (sum(list_victim_max_speed) / number_of_victims
                                if number_of_victims > 0 else 0)
    predator_average_max_speed = (sum(list_predator_max_speed) / number_of_predators
                                  if number_of_predators > 0 else 0)

    victim_average_satiety = (sum(list_victim_satiety) / number_of_victims
                              if number_of_victims > 0 else 0)
    predator_average_satiety = (sum(list_predator_satiety) / number_of_predators
                                if number_of_predators > 0 else 0)

    time_in_file = read_data('data.txt')[0]
    last_time_in_file = 0
    if len(time_in_file) > 0:
        last_time_in_file = max(time_in_file)

    if number_of_victims > 0 or number_of_predators > 0 or time > last_time_in_file:
        with open('data.txt', 'a') as file:
            cell_data = [str(time),
                         str(number_of_victims),
                         str(number_of_predators),
                         str(victim_average_age),
                         str(predator_average_age),
                         str(victim_average_max_speed),
                         str(predator_average_max_speed),
                         str(victim_average_satiety),
                         str(predator_average_satiety),
                         ]
            cell_data = ' '.join(cell_data)
            cell_data = cell_data + '\n'
            file.write(cell_data)


def read_data(file_name):
    """ Function reads data from 'file_name' file

    Parameters
    ----------
    file_name : string
        name of the data file
    Returns
    ----------
    victims_list : list
        list of the victim's population at the particular moment in time
    predators_list : list
        list of the predator's population at the particular moment in time
    time : list
        list of the particular moments
    """
    time_list = []
    input_data = []
    victims_list = []
    predators_list = []
    victims_list_mid_age = []
    predators_list_mid_age = []
    victims_list_mid_engine = []
    predators_list_mid_engine = []
    victims_list_mid_satiety = []
    predators_list_mid_satiety = []

    with open(file_name, 'r') as file:
        for line in file:
            input_data.append(line.split())
    for i in range(1, len(input_data)):
        time_list.append(int(input_data[i][0]))
        victims_list.append(int(input_data[i][1]))
        predators_list.append(int(input_data[i][2]))
        victims_list_mid_age.append(float(input_data[i][3]))
        predators_list_mid_age.append(float(input_data[i][4]))
        victims_list_mid_engine.append(float(input_data[i][5]))
        predators_list_mid_engine.append(float(input_data[i][6]))
        victims_list_mid_satiety.append(float(input_data[i][7]))
        predators_list_mid_satiety.append(float(input_data[i][8]))

    return (time_list,
            victims_list, predators_list,
            victims_list_mid_age, predators_list_mid_age,
            victims_list_mid_engine, predators_list_mid_engine,
            victims_list_mid_satiety, predators_list_mid_satiety,
            )


def clean_file(file_name):
    """ Function cleans 'data.txt' file

    Parameters
    ----------
    file_name : string
        name of the data file
    Returns
    ----------
    """
    file = open(file_name, 'w')
    file.close()


def delete_file(file_name):
    """ Function delete 'data.txt' file

    Parameters
    ----------
    file_name : string
        name of the data file
    Returns
    ----------
    """
    os.remove(file_name)
