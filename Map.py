import pygame
import constants as c
import Towers
import tools as t
import HUD
import enemies

class GameMap(object):
    def __init__(self):
        self.map = []

    def writemap(self, text):
        self.map = text


map = GameMap()


def createmap():
    file = open('Maps/map1.txt')
    filemap = list(file.readlines())
    file.close
    map1 = []
    for char in filemap:
        map1.append(list(char))
    for i in range(len(map1)):
        for z in range(len(map1[i])):
            if map1[i][z] == "#":
                map1[i][z] = "# "      # Spaces so that the two character turret names dont mess it up
            elif map1[i][z] == "-":
                map1[i][z] = "- "

    map.writemap([[x for x in s if x == "- " or x == "# "] for s in map1])
    c.Spawny = t.getspawny()
    if c.debugmap:
        print (c.Spawny)

def tiledpos(pos):
    position = list(pos)
    x = position[0] / 40
    y = position[1] / 40
    return x, y


def readmap():
    c.gameDisplay.fill(c.BLACK)
    for y in range(len(map.map)):
        for x in range(len(map.map[y])):
            if str(map.map[y][x]) == '- ':
                t.drawrec(x * 40, y * 40, 39, 39, c.MID_GREEN)
            elif str(map.map[y][x]) == '# ':
                t.drawrec(x * 40, y * 40, 39, 39, c.BROWN)
            elif str(map.map[y][x]) == 'a1':
                t.drawrec(x * 40, y * 40, 39, 39, c.MID_GREEN)
                c.gameDisplay.blit(pygame.image.load('Resources/Towers/archerbase1.png'), (x * 40, y * 40))
            elif str(map.map[y][x]) == 'a2':
                t.drawrec(x * 40, y * 40, 39, 39, c.MID_GREEN)
                c.gameDisplay.blit(pygame.image.load('Resources/Towers/archerbase2.png'), (x * 40, y * 40))
            elif str(map.map[y][x]) == 'a3':
                t.drawrec(x * 40, y * 40, 39, 39, c.MID_GREEN)
                c.gameDisplay.blit(pygame.image.load('Resources/Towers/archerbase3.png'), (x * 40, y * 40))
            elif str(map.map[y][x]) == 'a4':
                t.drawrec(x * 40, y * 40, 39, 39, c.MID_GREEN)
                c.gameDisplay.blit(pygame.image.load('Resources/Towers/archerbase4.png'), (x * 40, y * 40))
            elif str(map.map[y][x]) == 'a5':
                t.drawrec(x * 40, y * 40, 39, 39, c.MID_GREEN)
                c.gameDisplay.blit(pygame.image.load('Resources/Towers/archerbase5.png'), (x * 40, y * 40))
            elif str(map.map[y][x]) == 'b1':
                t.drawrec(x * 40, y * 40, 39, 39, c.MID_GREEN)
                c.gameDisplay.blit(pygame.image.load('Resources/Towers/tower1.png'), (x * 40, y * 40))
            elif str(map.map[y][x]) == 'b2':
                t.drawrec(x * 40, y * 40, 39, 39, c.MID_GREEN)
                c.gameDisplay.blit(pygame.image.load('Resources/Towers/tower2.png'), (x * 40, y * 40))
            elif str(map.map[y][x]) == 'b3':
                t.drawrec(x * 40, y * 40, 39, 39, c.MID_GREEN)
                c.gameDisplay.blit(pygame.image.load('Resources/Towers/tower3.png'), (x * 40, y * 40))
            elif str(map.map[y][x]) == 'b4':
                t.drawrec(x * 40, y * 40, 39, 39, c.MID_GREEN)
                c.gameDisplay.blit(pygame.image.load('Resources/Towers/tower4.png'), (x * 40, y * 40))
            elif str(map.map[y][x]) == 'b5':
                t.drawrec(x * 40, y * 40, 39, 39, c.MID_GREEN)
                c.gameDisplay.blit(pygame.image.load('Resources/Towers/tower5.png'), (x * 40, y * 40))
            else:
                t.drawrec(x * 40, y * 40, 39, 39, c.MID_GREEN)



def changemap(name, x, y):
    map.map[y][x] = name
    if c.debugmap:
        print ("Done")
        print (map.map[y][x])
        for i in range(len(map.map)):
            print (c.space.join(map.map[i]))


def mapclick(pos):
    if HUD.hudvars.selecteditem != "":
        HUD.clearselecteditem()
    if HUD.hudvars.selectedenemyid != "":
        HUD.clearselecteditem()

    x = t.listx(pos)
    y = t.listy(pos)

    if c.debugmap:
        print (Towers.towerspriteids)

    for enemy in enemies.zenemies:
        if c.debugmap:
            print("Checking " + str(pos))
        enemy.clickcheck(pos)


    for item in HUD.buttonlist:
        if map.map[y][x] == item.name:
            HUD.hudvars.selecteditem = item
            HUD.hudvars.selecteditemx = x
            HUD.hudvars.selecteditemy = y
            for sprites in Towers.towerspriteids:
                if (sprites[2]) / 40 == x and (sprites[3]) / 40 == y:
                    HUD.hudvars.selecteditemid = sprites[1]
        else:
            if c.debugmap:
                print ("Nothing")



