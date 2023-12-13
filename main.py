cell_list, meal_list = [], []
time = 0
time_step = 1


from visual import *



def user_parameters():
    pass


def buttons(user_parameter_set):
    pass


def restart_the_game(user_parameter_set):
    pass


def main():
    """Main function of program. It creates a screen where cells lives and makes actions with them"""

    global time

    # Interface parameters
    user_parameter_set = user_parameters()

    # Buttons
    button_list = buttons(user_parameter_set)  # Creates a button list

    restart_the_game(user_parameter_set)  # Creates the cells and the meal lists
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



        # Draws meal on the screen
        draw_meal(meal_list, screen)
        # Draws cells on the screen
        draw_cells(cell_list, screen)

        # Draws interface objects
        draw_user_panel(screen, button_list)


        # Updates the screen
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
