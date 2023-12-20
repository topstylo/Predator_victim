import random
import numpy as np
from vis_module import *


def vec_module(vector):
    """:arg :   vector - type : numpy array

    Function returns the modulus of the vector

    """
    return (vector[0] ** 2 + vector[1] ** 2) ** 0.5


def calc_vector(object_1, object_2):
    """:arg :   object_1, object_2 - the objects between which a vector will be calculated,
                type : Cell or Food

    Function returns the vector between objects, type : numpy array

    """
    return - object_1.position + object_2.position


def calc_area(cell, list_food : list):
    """Function returns the vector aimed to the area with the most food
    :arg
        cell - on cell, type : cell
        list_food - list of food, type : list

    """
    vec_area = np.array([0.0, 0.0])
    # Calculating a vec_area direction
    for food in list_food:
        vector_to_food = calc_vector(cell, food)
        vec_area[0] += (vector_to_food[0] / vec_module(vector_to_food) ** 3)
        vec_area[1] += (vector_to_food[1] / vec_module(vector_to_food) ** 3)

    # Normalization of the vec_area
    if vec_module(vec_area) > 0:
        vec_area = vec_area / vec_module(vec_area)
        vec_area *= cell.max_speed

    return vec_area


def calc_force(vector):
    """:arg :   vector - type : numpy array
    Function returns the value of a force (type : numpy array) that applied to the cell

    """

    if vec_module(vector) == 0:
        force = np.array([0, 0])
    else:
        # The value of the force :
        force = vector / (vec_module(vector) / 5) ** 10

    if vec_module(force) > 10:
        force *= 10 / vec_module(force)

    return force


def probability_to_multiply():
    """Function returns float from (0, 1) """
    return random.uniform(0, 1)


class Cell:
    """The common class for all cells
    Parameters:
            multiply_skill : float : A skill to multiply
            age : float : An age of a cell
            __color : list : color of the cell
            size  : int : A size of the cell
            position  : numpy array : Cords of a center of the cell
            velocity : numpy array : velocity of the cell
            satiety : float : Satiety of a cell
            reproductive_age  : list :  Limit of the cell's age where the cell can multiply
            age_step  : float : It is added to the age every moment of time; how fast a cell gets older
            age_of_last_multiplication  : float or int : The last time when the cell multiplied
            reproductive_delay  : float : How long the cell need to wait before multiply
            __border_color  : list : A __color of the borderline of the cell
            __border_thickness  : int : A variable that responsible for a thickness of the border; when cell gets
            older borderline gets thicker
    Methods:
        init : Initializes class
        update : Updates the cells' states
        draw : Draws the cell on the surface
    """

    def __init__(self, age_step : float, multiply_skill : float, satiety_decrement : float):
        # Common property
        self.multiply_skill = multiply_skill
        self.age = 0
        self.size = 5
        self.position = np.array([SCREEN_WIDTH / 2 * random.uniform(0, 1),
                                  SCREEN_HEIGHT / 2 * random.uniform(0, 1)])
        self.velocity = np.array([1.0, 1.0])
        # Genetic code
        self.satiety = 1.0  # сытость
        self.satiety_decrement = satiety_decrement
        self.__color = WHITE
        self.age_step = age_step
        self.age_of_last_multiplication = 0
        self.reproductive_delay = 0.5
        self.__border_color = WHITE
        self.__border_thickness = 1

    def update(self):
        """ Function updates states of the cell, cell can not run outside the screen """
        # Updates position :
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Cell can not run outside the screen :
        if self.position[0] >= SCREEN_WIDTH:
            self.position[0] = SCREEN_WIDTH - (self.position[0] - SCREEN_WIDTH)
            self.velocity[0] *= -1
        elif self.position[0] <= 0:
            self.position[0] = abs(self.position[0])
            self.velocity[0] *= -1

        if self.position[1] >= SCREEN_HEIGHT:
            self.position[1] = SCREEN_HEIGHT - (self.position[1] - SCREEN_HEIGHT)
            self.velocity[1] *= -1
        elif self.position[1] <= 0:
            self.position[1] = abs(self.position[1])
            self.velocity[1] *= -1
        
        self.age +=self.age_step
        self.satiety -= self.satiety_decrement
        self.__border___color = (102 + self.satiety * 153, 102 + self.satiety * 153,
                             102 + self.satiety * 153)
        if self.age < self.reproductive_age[0]:
            self.__border_thickness = -1
        elif self.reproductive_age[0] <= self.age <= self.reproductive_age[1]:
            self.__border_thickness = 1
        elif self.age > self.reproductive_age[1]:
            self.__border_thickness = 2

    def draw(self, surface):
        '''Draws the cell on the surface
           arg: surface : pygame.Surface : surface for drawing)
        '''
        position = [self.position[0], self.position[1] + PANEL_HEIGHT]
        pygame.draw.circle(
            surface,
            self.__color,
            position,
            self.size
        )
        pygame.draw.circle(
            surface,
            self.__border_color,
            position,
            self.size,
            self.__border_thickness
        )


class Predator(Cell):

    """ The class for predator cells. Is a child of Cell class
    The class for predator cells. Is a child of Cell class
    Parameters:
        satiety_decrement  : float : It is taken from satiety every moment of time; how fast satiety gets lower
        max_speed : float: A limit of the velocity the cell
        reproductive_age  : list :  Limit of the cell's age where the cell can multiply
        __color : list : A color of the cell
    Methods:
        __init__ : Initializes object
        calc_forces : Calculates the forces that applied to the cells
        multiply : Creating new cells
    """

    def __init__(self, age_step : float, multiply_skill : float, satiety_decrement : float):
        super().__init__(age_step, multiply_skill, satiety_decrement)
        self._Cell__color = RED
        self.max_speed = 3 + (2 * random.random() - 1) ** 3
        self.reproductive_age = [5, 50]
        self.reproductive_delay = 3

    def calc_forces(self, list_food, list_victims, list_predators):
        """:arg :   list_food - type : list, each element is Food type
                    list_cells - type : list, each element is Cell type

        Function calculates forces for a predator cell.
            It depends on how close the victims (victim cells), viscosity"""

        ''' For the predator cell. This block searches victims first of all in 100 radius, if there are nothing in
         300 radius and 600 radius. It helps avoid a lot of calculations'''

        closest_victims = [cell for cell in list_victims if vec_module(calc_vector(self, cell)) <= 100]

        if len(closest_victims) == 0:
            closest_victims = [cell for cell in list_victims if vec_module(calc_vector(self, cell)) <= 300]
        if len(closest_victims) == 0:
            closest_victims = [cell for cell in list_victims if vec_module(calc_vector(self, cell)) <= 600]

        closest_food = [food for food in list_food
                        if vec_module(calc_vector(self, food)) <= 100]
        if len(closest_food) == 0:
            closest_food = [food for food in list_food
                            if vec_module(calc_vector(self, food)) <= 300]
        if len(closest_food) == 0:
            closest_food = [food for food in list_food
                            if vec_module(calc_vector(self, food)) <= 600]
        # Calculating the force of entire engine
        # Gets direction of the vector to a food

        if len(closest_victims) != 0:
            acceleration_to_victims = calc_area(self, closest_victims)
        else:
            acceleration_to_victims = calc_area(self, closest_food)

        # Calculating the force of a viscosity
        viscosity = 0.5
        acceleration = - viscosity * np.array(self.velocity)
        acceleration += acceleration_to_victims
        # Calculating the repulsive force between two cells if they in the same class
        for cell in list_predators:
            if self != cell:
                vector_to_cell = calc_vector(self, cell)
                if vec_module(vector_to_cell) <= self.size:
                    acceleration -= calc_force(np.array(vector_to_cell))        
        self.velocity += acceleration

    def multiply(self, list_victims, list_predators, parameters):
        """:arg:     list_victims - list of cells
                     list_prdators - list of predators

        Function returns child_predator if it could spawn or 0 if it could not."""
        list_cells = list_victims+list_predators
        p = probability_to_multiply()  # The chance of a cell to multiply
        if (p > self.multiply_skill
                # Cells have to be if reproductive age to multiply :
                and self.reproductive_age[0] <= self.age <= self.reproductive_age[1]
                # Cells could not multiply each moment of time :
                and self.age - self.age_of_last_multiplication > self.reproductive_delay
                # Cells have to have a lot of satiety to multiply :
                and self.satiety >= 0.5):
            spawn = True
            phi = random.uniform(0, 2 * np.pi)  # Random phi
            x = self.position[0] + 2 * self.size * np.cos(phi)  # x cor of center new cell
            y = self.position[1] + 2 * self.size * np.sin(phi)  # y cor of center new cell

            for cell in list_cells:  # Do not spawn near each other
                vector = cell.position - np.array([x, y])
                module_vec = vec_module(vector)
                if module_vec <= 2 * self.size:
                    spawn = False
                    break
            if spawn:
                child_predator = Predator(parameters[2].value, parameters[3].value, parameters[4].value)  # Creates a new predator
                child_predator.position = np.array([x, y])
                self.satiety, child_predator.satiety = self.satiety / 2, self.satiety / 2
                list_predators.append(child_predator) # adding the born cell to the list
                return child_predator
            else:
                return 0
        else:
            return 0

    def update(self):
        super().update()
        self.__color = (150 + self.satiety * 102, 102 - self.satiety * 102,
                        102 - self.satiety * 102)


class Victim(Cell):
    """The class for victim cells. Is a child of Cell class
    Parameters:
            satiety_decrement  : float : It is taken from satiety every moment of time; how fast satiety gets lower
            max_speed : float: A limit of the velocity the cell
            reproductive_age  : list :  Limit of the cell's age where the cell can multiply
            __color : list : A color of the cell
            richness  : float : How much satiety a predator cell will get from eating a cell
            view_radius : float or int : How much a victim cell can see to find a predator
    Methods:
        init : Initializes object
        calc_forces : Calculates the forces that applied to the cells
        multiply : Creating new cells

    """


    def __init__(self, age_step : float, multiply_skill : float, satiety_decrement : float):
        super().__init__(age_step, multiply_skill, satiety_decrement)
        self.max_speed = 3 + (3 * random.random() - 1.5) ** 3
        self.reproductive_age = [5, 80]
        self.reproductive_delay = 0.5
        self._Cell__color = GREEN
        self.richness = 0.5 
        self.view_radius = 200

    def calc_forces(self, list_food, list_victims, list_predators):
        """:arg :   list_food - type : list, each element is Food type
                    list_victims - type : list, each element is Victim type
                    list_predators - tupe : list, each element is Predator type

        Function calculates forces for a victim cell.
                It depends on how close the food, how close predator to the cell, viscosity"""
        
        ''' This block searches food first of all in 100 radius, if there are nothing in
                 300 radius and 600 radius. It helps avoid a lot of calculations'''
        closest_food = [food for food in list_food
                        if vec_module(calc_vector(self, food)) <= 100]
        if len(closest_food) == 0:
            closest_food = [food for food in list_food
                            if vec_module(calc_vector(self, food)) <= 300]
        if len(closest_food) == 0:
            closest_food = [food for food in list_food
                            if vec_module(calc_vector(self, food)) <= 600]

        # It searches the nearest enemies
        closest_predators = [cell for cell in list_predators 
                             if vec_module(calc_vector(self, cell)) <= self.view_radius]

        # Calculating the force of entire engine
        # Gets direction of the vector to a food
        
        acceleration_to_food = calc_area(self, closest_food)
        
        # Calculating the force of a viscosity
        viscosity = 0.5
        acceleration = - viscosity * np.array(self.velocity)

        # Calculating the repulsive force between two cells if they in the same class
        for cell in list_victims:
            if self != cell:
                vector_to_cell = calc_vector(self, cell)
                if vec_module(vector_to_cell) <= self.size:
                    acceleration -= calc_force(np.array(vector_to_cell))

        # Calculating the force of a victim from a predator chasing after him
        list_of_danger = []
        list_of_danger = [cell for cell in closest_predators if vec_module(calc_vector(cell, self)) < 40]

        vec_area = - calc_area(self, list_of_danger)
        acceleration_from_predator = vec_area

        if len(list_of_danger) > 0:
            acceleration += acceleration_from_predator
        else:
            acceleration += acceleration_to_food

        self.velocity += acceleration

    def multiply(self, list_victims,list_predators, parameters):
        """:arg:     list_victims - list of victims
                     list_predators - list of predators

        Function returns child_victim if it could spawn or 0 if it could not."""
        p = probability_to_multiply()
        list_cells = list_victims + list_predators
        if (p > self.multiply_skill
                # Cells have to be in reproductive age to multiply :
                and self.reproductive_age[0] <= self.age <= self.reproductive_age[1]
                # Cells could not multiply each moment of time :
                and self.age - self.age_of_last_multiplication > self.reproductive_delay
                # Cells have to have a lot of satiety to multiply :
                and self.satiety >= 0.5):
            spawn = True
            child_victim = Victim(parameters[2].value, parameters[3].value, parameters[4].value)  # Creates a new predator

            phi = random.uniform(0, 2 * np.pi)  # Random phi
            x = self.position[0] + 2 * self.size * np.cos(phi)  # x cor of center new cell
            y = self.position[1] + 2 * self.size * np.sin(phi)  # y cor of center new cell

            for cell in list_cells:  # Do not spawn near each other
                vector = cell.position - np.array([x, y])
                module_vec = vec_module(vector)
                if module_vec <= 2 * self.size:
                    spawn = False
                    break
            if spawn:
                child_victim = Victim(parameters[2].value, parameters[3].value, parameters[4].value)  # Creates a new victim
                child_victim.position = np.array([x, y])
                self.satiety, child_victim.satiety = self.satiety / 2, self.satiety / 2
                list_victims.append(child_victim) # adding the born cell to the list
                return child_victim
            else:
                return 0
        else:
            return 0
    def update(self):
        super().update()
        self.__color = (102 - self.satiety * 102, 150 + self.satiety * 102,
                        102 - self.satiety * 102)


class Food:
    """The common class for food
    Parameters:
            position : numpy array : The position of the food on the screen
            size : int : The size of the food
            richness : float (from 0 to 1) : How much a victim cell gets satiety after eating a food
    Methods:
        init : Initializes class
        eaten : Shows was a food eaten or not

    """

    def __init__(self):
        self.position = np.array([random.uniform(0, 1) * SCREEN_WIDTH,
                                  random.uniform(0, 1) * SCREEN_HEIGHT])
        self.size = 3
        self.richness = random.uniform(0, 1)

    def draw(self,surface):
        x_min = self.position[0] - self.size / 2
        y_min = PANEL_HEIGHT + self.position[1] - self.size / 2
        pygame.draw.rect(
            surface,
            WHITE,
            [x_min, y_min, self.size, self.size]
        )

    def eaten(self, cell):
        """:arg :   cell - type : Cell. The cell that can eat the food

        Function returns True or False, depending on how much the cell is close to the food.

        """
        return vec_module(calc_vector(self, cell)) <= self.size + cell.size
