import pygame
import numpy as np

# Interface size

# Instrumental panel size
PANEL_HEIGHT = 50
# Simulating area size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
# Plot area size
PLOT_AREA_WIDTH = 600
PLOT_AREA_HEIGHT = 600

# Full screen size
WIDTH = SCREEN_WIDTH + PLOT_AREA_WIDTH
HEIGHT = PANEL_HEIGHT + SCREEN_HEIGHT

# Color set
WHITE = (255, 255, 255)
DARK_GREY = (102, 102, 102)
LIGHT_GREY = (204, 204, 204)
BLACK = (0, 0, 0)
RED = (204, 0, 0)
GREEN = (0, 204, 0)
BLUE = (0, 0, 204)

# Fonts
FONT = 'verdana'
FONT_COLOR = WHITE
FONT_SIZE_MIN = 10
FONT_SIZE_MAX = 14

# Axes
AXES_COLOR = WHITE


class UserPanelParameter:
    """ UserPanelParameter class : class for parameters which is controlled by user

        Parameters:
            name : string : name of parameter
            value : int or float : numeric value of parameter
            min_value : int or float : minimum for value
            max_value : int or float : maximum for value
            step_value : int or float : step of value changing
        Methods:
            init : Initializing function
            draw : Function draws buttons on the screen
            get_corner : Function calculates the corner coordinates of button
        """
    def __init__(self, name, value, min_value, max_value, step_value):
        """ Initializing function.

            :param name : string : name of parameter
            :param value : int or float : numeric value of parameter
            :param min_value : int or float : minimum for value
            :param max_value : int or float : maximum for value
            :param step_value : int or float : step of value changing
        """
        self.name = name
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.step_value = step_value

    def increase(self):
        """ Function increase the parameter value on one step_value. """
        self.value += self.step_value
        if self.value > self.max_value:
            self.value = self.max_value

    def increase_modulo(self):
        """ Function increase by modulo max_value the parameter value on one step_value. """
        self.value = (self.value + self.step_value) % (self.max_value + 1)

    def decrease(self):
        """ Function decrease the parameter value on one step_value. """
        self.value -= self.step_value
        if self.value < self.min_value:
            self.value = self.min_value


class Button:
    """ Button class : class of the button for user panel on the screen.

        Parameters:
            position : list : x and y coordinates of left top corner
            size : list : length and height of button
            function : string : python code that should be done after click
            text : string : text on the button
            parameter : UserPanelParameter : parameter, which is controlled
                by the button
        Methods:
            init : Initializes class
            draw : Draws buttons on the screen
            get_corner : Calculates the corner coordinates of button
    """
    def __init__(self, position, size, function, text, parameter):
        """ Initializing function.

            :param position : list : x and y coordinates of left top corner
            :param size : list : length and height of button
            :param function : string : python code that should be done after click
            :param text : string : text on the button
            :param parameter : UserPanelParameter : parameter, which is controlled
                by the button
        """
        self.position = position
        self.size = size
        self.function = function
        self.text = text
        self.parameter = parameter

    def draw(self, surface):
        """ Function draws buttons on the screen.

            :param surface : pygame.Surface : surface where button will be drawn
            """
        color_set = [WHITE, LIGHT_GREY, DARK_GREY, BLACK]
        # changes color if button not switch
        color = color_set[0]
        pygame.draw.rect(surface, color,
                         [self.position[0], self.position[1],
                          self.size[0], self.size[1]])
        font_surface = pygame.font.SysFont(FONT, FONT_SIZE_MIN)
        text_surface = font_surface.render(str(self.text), True, BLACK)
        text_rect = text_surface.get_rect(
            center=(self.position[0] + self.size[0] // 2,
                    self.position[1] + self.size[1] // 2))
        surface.blit(text_surface, text_rect)

    def get_corner(self, corner_name):
        """ Function calculates the corner coordinates of button.

        :param corner_name : string : name of corner
            ("top-left", "bottom-left", "top-right", "bottom-right")
            """
        if corner_name == "top-left":
            coordinate = self.position
        elif corner_name == "bottom-left":
            coordinate = [self.position[0],
                          self.position[1] + self.size[1]]
        elif corner_name == "top-right":
            coordinate = [self.position[0] + self.size[0],
                          self.position[1]]
        else:
            coordinate = [self.position[0] + self.size[0],
                          self.position[1] + self.size[1]]
        return coordinate


def clean_screen(surface):
    """ Function draw only background color on the surface

        :param surface : pygame.Surface : surface for cleaning
    """
    surface.fill(DARK_GREY)


def draw_user_panel(surf, button_list):
    """ Function draws user panel on the screen with all buttons.

        :param surf : pygame.Surface : surface where user panel will be drawn
        :param button_list : list(Button) : list, each element is Button type
    """
    pygame.draw.rect(
        surf,
        LIGHT_GREY,
        [0, 0, WIDTH, PANEL_HEIGHT]
    )

    for button in button_list:
        button.draw(surf)

def draw_cells(list_cells, surface):
    """ Function draws a cells on the surface.

        :param surface: pygame.Surface : surface for drawing
        :param list_cells : list(Cell) : list of cells
    """
    for cell in list_cells:
        cell.draw(surface)


def draw_food(food_list, surface):
    """ Function draws a food object on the surface.

        :param surface : pygame.Surface : surface where cells will be drawn
        :param food_list : list : list of food objects
        """
    for food in food_list:
        food.draw(surface)
