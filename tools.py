import pygame
import constants as c
import Map


def drawrec(x, y, w, h, color):
    pygame.draw.rect(c.gameDisplay, color, [x, y, w, h])


def drawhitbox(color, pos, radius, width):
    pygame.draw.circle(c.gameDisplay, color, (pos), radius + 25, width)


def drawimage(image, x, y):
    c.gameDisplay.blit(pygame.image.load(image), (x, y))


def rot_center(image, angle):
    """rotate a Surface, maintaining position."""

    loc = image.get_rect().center  # rot_image is not defined
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite


def drawcentered(image, pos):
    position = list(pos)
    x = position[0] - 20
    y = position[1] - 20
    c.gameDisplay.blit(pygame.image.load(image), (x, y))


def getspawny():
    for i in range(len(Map.map.map)):
        if Map.map.map[i][0] == "# ":
            print (i)
            return (40 * i)
        else:
            print ("Not in " + str(i))


def eztext(text, size, color, x, y):
    default_font = pygame.font.get_default_font()
    font_renderer = pygame.font.Font(default_font, size)

    label = font_renderer.render(
        text,  # The font to render
        1,  # With anti aliasing
        color)  # RGB Color
    # To apply this surface to another you can do the following
    c.gameDisplay.blit(
        label,  # The text to render
        (x, y))  # Where on the destination surface to render said font
def listx(pos):
    position = list(pos)
    x = int(pos[0] / 40)
    return x


def listy(pos):
    position = list(pos)
    y = int(pos[1] / 40)
    return y