from actions import *
from cell_classes import *
from vis_module import*

list_victims, list_predators, food_list = [], [], []
time = 0
time_step = 1

def add_victim(position, victims, parameters):
    """ Function adds the new victim cell to the place,
        where mouse was clicked.

        :param position : list : position of event
        :param victims : list(Victim) : list of victims
        :param parameters : list(UserPanelParameter) : user parameters
    """

    # Do not spawn cells outside screen
    if (position[0] > SCREEN_WIDTH or position[0] < 0
            or position[1] > SCREEN_HEIGHT or position[1] < 0):
        pass
    # Adds new cell
    else:
        # Creates cell
        new_victim = Victim(parameters[2].value, parameters[3].value, parameters[4].value)
        new_victim.position = position  # Generates random cell's position
        new_victim.age = random.random() * 50  # Generates random cell's age
        new_victim.satiety = random.random()  # Generates random cell's satiety
        victims.append(new_victim)


def add_predator(position, predators, parameters):
    """ Function adds the new predator cell in the place,
        where mouse clicks.

        :param position : list : position of event
        :param predators : list(Predator) : list of predators
        :param parameters : list(UserPanelParameter) : user parameters
    """

    # Do not spawn cells outside screen
    if (position[0] > SCREEN_WIDTH or position[0] < 0
            or position[1] > SCREEN_HEIGHT or position[1] < 0):
        pass
    else:
        # Creates cell
        new_predator = Predator(parameters[2].value, parameters[3].value, 0.005)
        # Generates random cell position
        new_predator.position = position
        new_predator.age = random.random() * 20
        new_predator.max_speed = 3 + (2 * random.random() - 1) ** 3
        new_predator.satiety = random.random()
        new_predator.reproductive_age = [20, 50]
        new_predator.reproductive_waiting = 3
        predators.append(new_predator)



def restart_the_game(parameters):
    """ Function returns cell_list with 50 different victim cells and 20 predators
        and the food_list.

        :param parameters : list(UserPanelParameter) : user parameters
    """
    global list_victims, list_predators, food_list, time, time_step

#    clean_file(file_name='data.txt')
    time = 0
    time_step = 1
    list_victims, list_predators = [],[]
    for i in range(50):
        position = np.array([random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT])
        add_victim(position, list_victims, parameters)
    for i in range(20):
        position = np.array([random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT])
        add_predator(position, list_predators, parameters)
    food_list = [Food()]


def user_parameters():
    """ Function creates user parameter set for user panel. """
    graph_number_parameter = UserPanelParameter('Номер графика', 0, 0, 3, 1)
    max_food_quantity_parameter = UserPanelParameter('Макс. кол-во еды', 20, 0, 200, 1)
    age_step_parameter = UserPanelParameter('Шаг старения', 3e-2, 0, 0.5, 1e-3)
    multiply_skill_parameter = UserPanelParameter('Сложность размножения', 0.8, 0, 1, 0.01)
    satiety_step_parameter = UserPanelParameter('Шаг сытости', 3e-3, 0, 0.5, 1e-4)
    return [graph_number_parameter,
            max_food_quantity_parameter,
            age_step_parameter,
            multiply_skill_parameter,
            satiety_step_parameter]


def update_labels(labels, parameters):
    """ Function updates text values in buttons that indicates
        the current values of user parameters.

        :param labels : list(Button) : list of buttons that indicates values
        :param parameters : list(UserPanelParameter) : list of parameters
    """
    round_set = [0, 3, 2, 4]
    for i in range(len(labels)):
        labels[i].text = round(parameters[i].value, round_set[i])


def update_parameters(parameters, cells):
    """ Function updates values of current parameters after changing.

        :param parameters : list(UserPanelParameter) : list of parameters
        :param cells : list(Cell) : list of cell
    """
    for cell in cells:
        cell.age_step = parameters[2].value
        cell.multiply_skill = parameters[3].value
        cell.satiety_step = parameters[4].value


def main():
    """Main function of program. It creates a screen where cells lives and makes an actions with them"""

    global time

    # Interface parameters
    user_parameter_set = user_parameters()

    restart_the_game(user_parameter_set)  # Creates the cells and the food lists
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.set_alpha(None)
    clock = pygame.time.Clock()
    fps = 100
    finished = False
    while not finished:
        time += time_step
        clean_screen(screen)
        clock.tick(fps)
        # Checks the users actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Checks if the right button of the mouse is clicked
                if event.button == 1:
                    # Adds a victim cell
                    add_victim(np.array([event.pos[0], event.pos[1] - PANEL_HEIGHT]),
                                 list_victims,
                                 user_parameter_set)
                    # Calls a find_button function
                    find_button(event.pos, button_list, user_parameter_set)
                    # Checks if the left button of the mouse is clicked
                    update_labels(labels=button_list[3::4],
                                  parameters=user_parameter_set[1:])
                    update_parameters(user_parameter_set, list_victims+list_predators)
                elif event.button == 3:
                    # Adds a predator
                    add_predator(np.array([event.pos[0], event.pos[1] - PANEL_HEIGHT]),
                                 list_predators,
                                 user_parameter_set)

        if time_step != 0:
            # Update all data for one time step
            if len(food_list) < user_parameter_set[1].value:
                food_list.append(Food())
            multiply(list_victims,list_predators, time, user_parameter_set)
            update(list_victims, list_predators, food_list, time)

        # Draws food on the screen
        draw_food(food_list, screen)
        # Draws cells on the screen
        draw_cells(list_victims+list_predators, screen)

        # Updates the screen
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
