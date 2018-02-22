import pygame
import constants as c
import HUD
import Map
import stats
import wave
import enemies
import Towers
import projectile

pygame.init()


pygame.display.set_caption('Castle Defender')
clock = pygame.time.Clock()


def mainmenu():
    mainmenu = True

    while mainmenu:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        c.gameDisplay.fill(c.WHITE)
        pygame.display.update()
        clock.tick(15)


def gameloop():
    Map.createmap()
    for i in range(len(Map.map.map)):
        print (c.space.join(Map.map.map[i]))
    while game:
        eventlistener()
        Map.readmap()
        HUD.hud()
        wave.wavelistener()
        Towers.placedtowers.update()
        projectile.projectiles.update()
        projectile.projectiles.draw(c.gameDisplay)
        Towers.placedtowers.draw(c.gameDisplay)
        stats.stats.miliseconds = pygame.time.get_ticks()
        pygame.display.update()
        clock.tick(60)


def eventlistener():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global game
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if HUD.inhudrange(pygame.mouse.get_pos()):
                HUD.hudclick(pygame.mouse.get_pos())
            else:
                Map.mapclick(pygame.mouse.get_pos())


if __name__ == '__main__':
    game = True
    gameloop()
    pygame.quit()

