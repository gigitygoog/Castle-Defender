import pygame
import constants as c
import Towers
import Map
import tools as t
import stats
import wave
import projectile

pygame.font.init()



def inhudrange(pos):
    position = list(pos)
    if position[1] >= 600:
        return True
    else:
        return False


class hudvars(object):
    selecteditem = ""
    selecteditemx = ""
    selecteditemy = ""
    selecteditemid = ""
    selecteditemidkill = ""
    selecteditemreal = ""

    selectedenemy = ""
    selectedenemyid = ""


def hud():
    t.drawrec(0, c.display_height - 200, c.HUD_W, c.HUD_H, c.LIGHT_BLUE)
    t.drawrec(0, c.display_height - 200, c.HUD_W, 10, c.NEAR_BLACK_BLUE)
    t.drawimage('Resources/HUD.png', 0, 600)

    t.eztext("Wave: " + str(stats.stats.wave), 24, c.NEAR_BLACK, 60, 620)
    t.eztext("Gold:  " + str(stats.stats.gold), 24, c.NEAR_BLACK, 60, 650)
    t.eztext("Time to wave: " + stats.stats.gettime(), 24, c.NEAR_BLACK, 60, 680)


    t.drawrec(319, c.display_height - 180, 1, 200, c.NEAR_BLACK_BLUE) # turret info
    t.drawrec(319, c.display_height - 180, 241, 1, c.NEAR_BLACK_BLUE)
    t.drawrec(560, c.display_height - 180, 1, 200, c.NEAR_BLACK_BLUE)

    t.drawrec(600, c.display_height - 180, 1, 200, c.NEAR_BLACK_BLUE) # turret box
    t.drawrec(600, c.display_height - 180, 520, 1, c.NEAR_BLACK_BLUE)
    t.drawrec(1120, c.display_height - 180, 1, 200, c.NEAR_BLACK_BLUE)
    t.eztext("Towers:", 24, c.NEAR_BLACK, 610, c.display_height - 170)

    if hudvars.selecteditem != "":
        turretinfo(hudvars.selecteditem)
    if hudvars.selectedenemy != "":
        enemyinfo(hudvars.selectedenemy)
#    t.eztext(str(stats.stats.gettime()), 24, c.NEAR_BLACK, 60, 710)
    for item in buttonlist: # Puts up a button to buy it.
        if item.level == '1':
            c.gameDisplay.blit(pygame.image.load(item.img1), (item.x, item.y))
            c.gameDisplay.blit(pygame.image.load(item.realimage), (item.x, item.y))
            if len(str(item.price)) == 2:
                t.eztext(str(item.price), 22, c.NEAR_BLACK, item.x + 8, (item.y + 45))
            else:
                t.eztext(str(item.price), 22, c.NEAR_BLACK, item.x + 2, (item.y + 45))


def turretinfo(turret):
    if turret == hudvars.selecteditem:
        t.eztext(turret.displayname + " level " + turret.level, 18, c.BLACK, 340, 625)
        t.eztext("AOE:       " + str(turret.aoe), 20, c.BLACK, 340, 655)
        t.eztext("Speed:    " + str(getspeed(turret)), 20, c.BLACK, 340, 675)
        t.eztext("Range:   " + str(turret.range), 20, c.BLACK, 340, 695)
        t.eztext("Damage: " + str(turret.damage), 20, c.BLACK, 340, 715)
        if not Towers.checkselected(turret):
         #   t.drawhitbox(c.DARK_GREEN, (int(hudvars.selecteditemx) * 40 + 20, int(hudvars.selecteditemy) * 40 + 20), turret.range,
         #                1)
            t.drawrec(428, 744, 60, 20, c.RED) # sell
            if turret.upgradeprice != None:
                t.drawrec(428, 765, 60, 20, c.GREEN)  # Upgrade
        t.eztext("Sell:        " + str(int(turret.price * 0.80)), 20, c.BLACK, 340, 745)
        if turret.upgradeprice == None:

            t.eztext("Max Level", 20, c.BLACK, 340, 765)

        else:
            t.eztext("Upgrade:" + str(turret.upgradeprice), 20, c.BLACK, 340, 765)

def enemyinfo(enemy):
    if enemy.health < 1:
        clearselecteditem()
    if enemy == hudvars.selectedenemy:
        t.eztext(enemy.displayname + " level " + str(enemy.level), 18, c.BLACK, 340, 625)
        t.eztext("Health:   " + str(enemy.health), 20, c.BLACK, 340, 655)
        t.eztext("Speed:    " + str(getspeed(enemy)), 20, c.BLACK, 340, 675)
        c.gameDisplay.blit(pygame.image.load(enemy.imagelink), (500, 655))
    else:
        print ("Something went wrong hud line 77")


class buttons(object):
    def __init__(self, name, displayname, level, img1, realimage, img2, img3, x, y, selected, damage, range, speed, aoe, price,
                 upgradeprice, realtower, nexttower):
        self.name = name
        self.displayname = displayname
        self.level = level
        self.img1 = img1
        self.realimage = realimage
        self.img2 = img2
        self.img3 = img3
        self.x = x
        self.y = y
        self.selected = selected
        self.range = range
        self.damage = damage
        self.speed = speed
        self.aoe = aoe
        self.price = price
        self.upgradeprice = upgradeprice
        self.realtower = realtower
        self.nexttower = nexttower

    def isselected(self):
        while self.selected:
            Map.readmap()
            hud()
            wave.wavelistener()
            Towers.placedtowers.update()
            projectile.projectiles.update()
            projectile.projectiles.draw(c.gameDisplay)
            Towers.placedtowers.draw(c.gameDisplay)
            t.drawhitbox(c.DARK_GREEN, (pygame.mouse.get_pos()), self.range, 1)
            c.gameDisplay.blit(pygame.image.load(self.img2), (self.x, self.y))  # menu green turret

            if Towers.canplace(pygame.mouse.get_pos()):
                t.drawcentered(self.img2, (pygame.mouse.get_pos()))  # the moving green turret
            else:
                t.drawcentered(self.img3, (pygame.mouse.get_pos()))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if Towers.canplace(pygame.mouse.get_pos()):
                            Towers.placetower(self, t.listx(pygame.mouse.get_pos()), t.listy(pygame.mouse.get_pos()))
                            hudvars.selecteditem = ""
                            self.selected = False
                    else:
                        hudvars.selecteditem = ""
                        self.selected = False
            stats.stats.miliseconds = pygame.time.get_ticks()
            pygame.display.update()

    def menuclicked(self):
        c.gameDisplay.blit(pygame.image.load(self.Img), pygame.mouse.get_pos())


archertower1b = buttons(
    'a1',
    'Archer Tower',
    '1',
    'Resources/Towers/archerbase1.png',
    'Resources/Towers/archer-tower1.png',
    'Resources/Towers/archer-tower1true.png',
    'Resources/Towers/archer-tower1false.png',
    640,
    c.display_height - 140,
    False, # selected, damage, range, speed, aoe, price
    25,
    150,
    1,
    0,
    50,
    100,
    Towers.archertower1,
    Towers.archertower2
)

archertower2b = buttons(
    'a2',
    'Archer Tower',
    '2',
    'Resources/Towers/archer-tower2.png',
    None,
    'Resources/Towers/archer-tower1hover.png',
    'Resources/Towers/tower1false.png',
    None,
    c.display_height - 140,
    False,# selected, damage, range, speed, aoe, price
    30,
    175,
    50,
    0,
    150,
    250,
    Towers.archertower2,
    Towers.archertower3

)

archertower3b = buttons(
    'a3',
    'Archer Tower',
    '3',
    'Resources/Towers/archer-tower3.png',
    None,
    'Resources/Towers/archer-tower1hover.png',
    'Resources/Towers/tower1false.png',
    None,
    c.display_height - 140,
    False,# selected, damage, range, speed, aoe, price, upgradeprice
    35,
    200,
    400,
    0,
    350,
    500,
    Towers.archertower3,
    Towers.archertower4
)

archertower4b = buttons(
    'a4',
    'Archer Tower',
    '4',
    'Resources/Towers/archer-tower4.png',
    None,
    'Resources/Towers/archer-tower1hover.png',
    'Resources/Towers/tower1false.png',
    None,
    c.display_height - 140,
    False,# selected, damage, range, speed, aoe, price, upgradeprice
    40,
    225,
    800,
    0,
    850,
    2000,
    Towers.archertower4,
    Towers.archertower5
)

archertower5b = buttons(
    'a5',
    'Archer Tower',
    '5',
    'Resources/Towers/archer-tower5.png',
    None,
    'Resources/Towers/archer-tower1hover.png',
    'Resources/Towers/tower1false.png',
    None,
    c.display_height - 140,
    False,# selected, damage, range, speed, aoe, price, upgradeprice
    40,
    250,
    800,
    0,
    2850,
    None,
    Towers.archertower5,
    None

)
ballistatower1b = buttons(
    'b1',
    'Ballista Tower',
    '1',
    'Resources/Towers/tower1.png',
    'Resources/Towers/ballista1.png',
    'Resources/Towers/tower1hover.png',
    'Resources/Towers/tower1false.png',
    700,
    c.display_height - 140,
    False,# selected, damage, range, speed, aoe, price
    300,
    250,
    20,
    0,
    800,
    800,
    Towers.ballistatower1,
    Towers.ballistatower2
)
ballistatower2b = buttons(
    'b2',
    'Ballista Tower',
    '2',
    'Resources/Towers/tower2.png',
    None,
    'Resources/Towers/tower1hover.png',
    'Resources/Towers/tower1false.png',
    None,
    None,
    False,# selected, damage, range, speed, aoe, price
    375,
    275,
    20,
    0,
    1600,
    1600,
    Towers.ballistatower2,
    Towers.ballistatower3
)
ballistatower3b = buttons(
    'b3',
    'Ballista Tower',
    '3',
    'Resources/Towers/tower3.png',
    None,
    'Resources/Towers/tower1hover.png',
    'Resources/Towers/tower1false.png',
    None,
    None,
    False,# selected, damage, range, speed, aoe, price
    300,
    500,
    20,
    0,
    3200,
    3200,
    Towers.ballistatower3,
    Towers.ballistatower4
)
ballistatower4b = buttons(
    'b4',
    'Ballista Tower',
    '4',
    'Resources/Towers/tower4.png',
    None,
    'Resources/Towers/tower1hover.png',
    'Resources/Towers/tower1false.png',
    None,
    None,
    False,# selected, damage, range, speed, aoe, price
    650,
    350,
    20,
    0,
    6400,
    6400,
    Towers.ballistatower4,
    Towers.ballistatower5
)
ballistatower5b = buttons(
    'b5',
    'Ballista Tower',
    '5',
    'Resources/Towers/tower5.png',
    None,
    'Resources/Towers/tower1hover.png',
    'Resources/Towers/tower1false.png',
    None,
    None,
    False,# selected, damage, range, speed, aoe, price
    1000,
    400,
    20,
    0,
    12800,
    None,
    Towers.ballistatower5,
    None
)

buttonlist = [archertower1b, archertower2b, archertower3b, archertower4b, archertower5b, ballistatower1b,
              ballistatower2b, ballistatower3b, ballistatower4b, ballistatower5b]


def clearselecteditem():
    hudvars.selecteditem = ""
    hudvars.selecteditemx = ""
    hudvars.selecteditemy = ""
    hudvars.selecteditemid = ""
    hudvars.selecteditemidkill = ""
    hudvars.selecteditemreal = ""
    hudvars.selectenemyid = ""
    hudvars.selectedenemy = ""


def getspeed(tower):
    if tower.speed >= 900:
        return "Fastest"
    elif tower.speed >= 600:
        return "Very Fast"
    elif tower.speed >= 300:
        return "Fast"
    elif 300 >= tower.speed > -100:
        return "Average"
    elif -100 >= tower.speed >= -500:
        return "Slow"
    elif -500 >= tower.speed:
        return "Very Slow"


def hudclick(pos):
    position = list(pos)
    if hudvars.selecteditem != "":
        item = hudvars.selecteditem
        if position[0] in range(428, 428 + 34) and position[1] in range(744, 744 + 20):
            sellitem(item)
            return True
        if position[0] in range(428, 428 + 40) and position[1] in range(765, 765 + 20):
            if item.upgradeprice != None:
                upgradeitem(item)
                return True
    for item in buttonlist:
        if item.x != None:
            if position[0] in range(item.x, item.x + 40) and position[1] in range(item.y, item.y + 40):
                clearselecteditem()
                if stats.stats.gold >= item.price:
                    hudvars.selecteditem = item
                    item.selected = True
                    if c.debugmap:
                        print ("GOOD TO GO")
                    item.isselected()
                else:
                    print ("Not enough money!")
    else:
        if c.debugmap:
            print ("Seemed to click nothing")
            print (position[0], range(item.x, item.x + 40), position[1], range(item.y, item.y + 40))


def sellitem(item):
    Map.changemap("- ", hudvars.selecteditemx, hudvars.selecteditemy)
    hudvars.selecteditemidkill = hudvars.selecteditemid
    Towers.placedtowers.update()
    stats.stats.gold += int(Towers.checkprice(item) * 0.80)
    clearselecteditem()


def upgradeitem(item):
    x = hudvars.selecteditemx
    y = hudvars.selecteditemy
    if item.level != 5:
        if stats.stats.gold >= int(Towers.checkupgradeprice(item)):
            new = getnewtower()
            Map.changemap(Towers.upgradename(item), hudvars.selecteditemx, hudvars.selecteditemy)
            stats.stats.gold -= int(Towers.checkupgradeprice(item))
            hudvars.selecteditemidkill = hudvars.selecteditemid
            Towers.placedtowers.add(new(hudvars.selecteditemx * 40, hudvars.selecteditemy * 40))
            Towers.placedtowers.update()
            clearselecteditem()
            Map.mapclick((x * 40, y * 40))
        else:
            print ("No money!")
    else:
        print ("Max Level")


def getnewtower():
    old = hudvars.selecteditem
    for item in buttonlist:
        if str(item.realtower) == str(old.realtower):
            new = item.nexttower
            return new
        else:
            continue
