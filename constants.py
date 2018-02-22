import pygame

display_width = 1200
display_height = 800

MAP_W = display_width
MAP_H = display_height - 200

HUD_W = display_width
HUD_H = 200

Spawny = 0
gameDisplay = pygame.display.set_mode((display_width, display_height))
space = " "
BLACK = 0, 0, 0
NEAR_BLACK = 1, 0, 0
WHITE = 255, 255, 255
BLACK_BLUE = 19, 15, 48
NEAR_BLACK_BLUE = 20, 15, 48
LIGHT_BLUE = 0, 153, 204
DARK_RED = 118, 27, 12
REALLY_DARK_RED = 15, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
MID_GREEN = 0, 150, 0
PINK = 208, 32, 144
DARK_GREEN = 0, 100, 0
BROWN = 222,184,135

debugpath = False
debugspawn = False
debugmap = False
hitboxes = False
debugtargeting = False