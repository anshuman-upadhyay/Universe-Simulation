#Making the on screen elements 
import pygame 
import utils.constants as c

# Window function
def create_window():
    screen=pygame.display.set_mode((c.WIDTH,c.HEIGHT))
    pygame.display.set_caption(c.TITLE)
    clock= pygame.time.Clock()
    return screen,clock

