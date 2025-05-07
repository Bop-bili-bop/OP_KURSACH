import pygame
from os.path import join
#FONT
def font_init(size):
    return pygame.font.Font(join('..', 'graphics', 'font.ttf'), size)