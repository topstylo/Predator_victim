from cells_classes import *
import numpy as np


def kill_the_cell(list_victims, list_predators, cell, time):
    """:arg:     list_cell - type : list. Contains all elements with type 'Cell'
                cell - type : Cell. A cell that was killed
                time - type : float. Moment of the time when the cell was killed

    Function removes cell from the list_cell and writes data about it

    """

    if cell in list_victims:
        list_victims.remove(cell)  # A cell removed from the list
    elif cell in list_predators:
        list_predators.remove(cell)


def multiply(list_victims : list,list_predators : list, time : float, parameters):
    """:arg:    list_cells - type : list. Contains all elements with type 'Cell'
                time -  type : float. How much time passed since the beginning of the simulation

    Function adds new cell (cells multiply) and kills cell if it is too old or too hungry

    """
    for cell in list_cells:
        if cell.age >= 100 or cell.satiety <= 0:  # A cell dies if it is too old or too hungry
            kill_the_cell(list_victims,list_predators, cell, time)
        cell.multiply(list_vectims,list_predators, parameters)  # 


def update(list_victims, list_predators, food_list, time):
    """:arg:    list_cells - type : list. Contains all elements with type 'Cell'
                food_list - type : list. Contains all elements with type 'Food'
                time - type : float. The moment of time when update is called

    Updates of cell's and food's positions on the screen;
    kills the peaceful cells if they are attacked by predator cell;
    adds age of cell and gets lower satiety of cell

    """
    list_cells = list_victims+list_predators # list af all cells
    for cell in list_cells:
        cell.calc_forces(food_list, list_cells)  # Calculates forces
        cell.update()  # Updates a position of the cells
        # Is a peaceful cell was eaten by a predator :
    for cell in list_predators:
        if len(list_victims) != 0:
            for victim in list_victims:
                # They are have to be close to each other :
                if vec_module(calc_vector(cell, victim)) <= victim.size:
                    # Kills a cell :
                    kill_the_cell(list_victims,list_predators, victim, time)
                    # Adds satiety :
                    cell.satiety += victim.richness
                    # Satiety have to be from 0 to 1 :
                    cell.satiety = min(cell.satiety, 1)


    # It checks was food eaten by peaceful cell or not:
    for food in food_list:

        food_eaten = False  # Special that responsible for eaten food

        for cell in list_victims:
            if food.eaten(cell):
                cell.satiety += food.richness
                cell.satiety = min(cell.satiety, 1)
                # Food removed from the list when it is eaten :
                food_list.remove(food)

                food_eaten = True
                break
        if food_eaten:
            break