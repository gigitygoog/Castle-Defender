import pygame
import constants as c
import Map
import tools as t
import stats
import HUD
import enemies
import projectile
import math

"""
class Tower(object):
    placedtowers = []
    def __init__(self, name, displayname, level, img1, img2, img3, x, y, selected, damage, range, speed, aoe, price,
                 upgradeprice):
        self.name = name
        self.displayname = displayname
        self.level = level
        self.img1 = img1
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

    def checkattack(self, x, y):
        if wave.Wave.isgoing:
            targetsinrange = Tower.gettargetsinrange(self, x, y)
            pass
    def gettargetsinrange(self, x, y):
        for sprite in iter(enemies.zenemies.sprites):
            if sprite.rect.x in range(x - self.range, x + self.range) and sprite.rect.y in range(y - self.range, y + self.range):
                print ("This sprite is in range: " + str(sprite.rect.x) + " " + str(sprite.rect.y))
                return sprite
    def isselected(self):
        while self.selected:
            Map.readmap()
            HUD.hud()
            wave.wavelistener()
            enemies.zenemies.draw(c.gameDisplay)
            c.gameDisplay.blit(pygame.image.load(self.img2), (self.x, self.y)) # menu green turret

            if canplace(pygame.mouse.get_pos()):
                t.drawcentered(self.img2, (pygame.mouse.get_pos()))        # the moving green turret
            else:
                t.drawcentered(self.img3, (pygame.mouse.get_pos()))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if canplace(pygame.mouse.get_pos()):
                            placetower(self, t.listx(pygame.mouse.get_pos()), t.listy(pygame.mouse.get_pos()))
                            HUD.hudvars.selecteditem = ""
                            self.selected = False
                    else:
                        HUD.hudvars.selecteditem = ""
                        self.selected = False
            stats.stats.miliseconds = pygame.time.get_ticks()
            pygame.display.update()

    def menuclicked(self):
        c.gameDisplay.blit(pygame.image.load(self.Img), pygame.mouse.get_pos())
"""
placedtowers = pygame.sprite.Group()
towerspriteids = []

class Tower(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        print("created a new sprite:", id(self))
        towerspriteids.append([self, id(self), self.rect.x, self.rect.y])
        self.target = None
        self.angle = 0
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.baseimage = self.image
        self.baserealimage = self.image
        self.baserect = self.rect
        self.isselected = False
        self.radius = self.range
        self.lastattacked = -1000
        self.lastrotated = 0

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.lastattacked + self.speed >= 600:
            self.baseimage = self.baserealimage

        if self.target != None:
            if pygame.sprite.collide_circle(self.target, self):
                self.getattack()
            else:
                self.target = None
            if self.rotate and self.target != None:
                if c.debugtargeting:
                    print (str(self.target))
                    print (str(self.target.rect.x))
                self.image, self.rect = self.rot_center(self.baseimage, self.baserect)
        else:
            self.target = None

        if c.hitboxes:
            t.drawhitbox(c.DARK_GREEN, (self.baserect.x + 20, self.baserect.y + 20), self.radius, 1)

        if HUD.hudvars.selecteditemidkill == id(self):
            print ("Killed " + str(id(self)))
            self.kill()

        if self.target == None or self.target.health < 1:
            self.gettarget()
        if HUD.hudvars.selecteditemid == id(self):
            self.isselected = True
        if self.isselected:
            if HUD.hudvars.selecteditemid != id(self):
                self.isselected = False
            else:
                t.drawhitbox(c.DARK_GREEN, (self.baserect.x + 20, self.baserect.y + 20), self.radius, 1)

    def rot_center(self, image, rect):
        """rotate an image while keeping its center"""
        angle = self.getangle()
        if c.debugtargeting:
            print ("Angle: " + str(angle))
        #rot_image = pygame.transform.rotate(image, angle)
        rot_image = pygame.transform.rotozoom(image, angle, 1)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect


    def getangle(self):
        if self.target.rect.x == None:
            if c.debugtargeting:
                print ("Target seems to be dead...")
            self.kill()
            return 0

        if (self.rect.y == self.target.rect.y or abs(self.rect.y - self.target.rect.y) < 15) and self.rect.x > self.target.rect.x: # Straight Left
           # self.angle = 90
          #  self.image = pygame.transform.rotate(self.baseimage, self.angle)
          #  self.lastrotated = self.angle
            return 90

        elif (self.rect.x == self.target.rect.x or abs(self.rect.x - self.target.rect.x)) < 15 and self.rect.y > self.target.rect.y: # Straight Up
            return 0


        elif (self.rect.y == self.target.rect.y or abs(self.rect.y - self.target.rect.y) < 15) and self.rect.x < self.target.rect.x: # Straight Right
            if c.debugtargeting:
                print ("Target has the same y as me. Going Right!")
            return -90


        elif (self.rect.x == self.target.rect.x or abs(self.rect.x - self.target.rect.x) < 15) and self.rect.y < self.target.rect.y: # Straight Down
            if c.debugtargeting:
                print ("Target has same x as me. Going Down!")
            return 180


        elif self.rect.x - self.target.rect.x >= 0 and self.rect.y - self.target.rect.y >= 0: #Top left triangle
            if c.debugtargeting:
                print ("I am trying top left triangle: " + str(self.rect.x) + " " + str(self.rect.y) + " " + str(self.target.rect.x) + " " + str(self.target.rect.y))

            adjacent = abs(self.rect.x - self.target.rect.x)
            opposite = abs(self.rect.y - self.target.rect.y)
            if c.debugtargeting:
                print ("Opposite: " + str(opposite))
                print ("Adjacent: " + str(adjacent))
            return 90 - math.degrees(math.atan(opposite / adjacent))
           # return int(90 - math.degrees(math.atan(opposite / adjacent)))


        elif self.target.rect.x - self.rect.x >= 0 and self.rect.y - self.target.rect.y >= 0: #Top right triangle
            if c.debugtargeting:
                print ("I am trying top right triangle: " + str(self.rect.x) + " " + str(self.rect.y) + " " + str(self.target.rect.x) + " " + str(self.target.rect.y))
            adjacent = abs(self.rect.x - self.target.rect.x)
            opposite = abs(self.rect.y - self.target.rect.y)
            return -90 + math.degrees(math.atan(opposite / adjacent))
          #  return int(-90 + math.degrees(math.atan(opposite / adjacent)))

        elif self.target.rect.x - self.rect.x >= 0 and self.target.rect.y - self.target.rect.y >= 0: #Bottom Right triangle
            if c.debugtargeting:
                print ("I am trying Bottom Right triangle: " + str(self.rect.x) + " " + str(self.rect.y) + " " + str(self.target.rect.x) + " " + str(self.target.rect.y))
            adjacent = abs(self.rect.x - self.target.rect.x)
            opposite = abs(self.rect.y - self.target.rect.y)
            return -90 - math.degrees(math.atan(opposite / adjacent))
          #  return int(-90 - math.degrees(math.atan(opposite / adjacent)))

        elif self.rect.x - self.target.rect.x >= 0 and self.target.rect.y - self.target.rect.y >= 0: #Bottom left triangle
            if c.debugtargeting:
                print ("I am trying Bottom left triangle: " + str(self.rect.x) + " " + str(self.rect.y) + " " + str(self.target.rect.x) + " " + str(self.target.rect.y))
            adjacent = abs(self.rect.x - self.target.rect.x)
            opposite = abs(self.rect.y - self.target.rect.y)
            return 90 + math.degrees(math.atan(opposite / adjacent))
         #   return int(90 + math.degrees(math.atan(opposite / adjacent)))
        else:
            if c.debugtargeting:
                print ("Error with targeting projectile.py line 135")
        #    print("me =" + str(self.rect.x) + "  " + str(self.rect.y))
        #    print("Them =" + str(self.target.rect.x) + "  " + str(self.target.rect.y ))

    def attack(self, target, attacks):
        attacks = attacks
        if attacks > 1:
            projectile.projectiles.add(self.projectile(self.rect.x, self.rect.y, target, self.damage, self.projectilespeed))
            projectile.projectiles.add(self.projectile(self.rect.x + 5, self.rect.y + 5, target, self.damage, self.projectilespeed))
        else:
            projectile.projectiles.add(self.projectile(self.rect.x, self.rect.y, target, self.damage, self.projectilespeed))

    def gettarget(self):
        self.target = None
        enemiesinrange = []
        for enemy in enemies.zenemies:
            if pygame.sprite.collide_circle(enemy, self):
                enemiesinrange.append(enemy)
                self.target = enemy
                break

    def getattack(self):
        now = pygame.time.get_ticks()
        if now - self.lastattacked + self.speed >= 1000:
            if self.rotate:
                self.baseimage = self.image2
            self.attack(self.target, self.attacks)
            self.lastattacked = now
        else:
            pass



    def menuclicked(self):
        c.gameDisplay.blit(pygame.image.load(self.Img), pygame.mouse.get_pos())


class archertower1(Tower):
    def __init__(self, x, y):
        self.image = pygame.image.load('Resources/Towers/archer-tower1.png')
        self.rotate = False
        self.selected = False
        self.projectile = projectile.arrow
        self.projectilespeed = 15
        self.range = 150
        self.damage = 25
        self.attacks = 1
        self.speed = 50
        self.aoe = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 50
        self.upgradeprice = 100
        self.buttonx = 640,  # button X
        self.buttony = c.display_height - 140,  # button Y
        super().__init__()
        self.shortname = 'a1',
        self.displayname = 'Archer Tower',
        self.level = '1'


class archertower2(Tower):
    def __init__(self, x, y):
        self.image = pygame.image.load('Resources/Towers/archer-tower1.png')
        self.rotate = False
        self.selected = False
        self.projectile = projectile.arrow
        self.projectilespeed = 15
        self.range = 175
        self.damage = 30
        self.attacks = 1
        self.speed = 400
        self.aoe = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 150
        self.upgradeprice = 200
        self.buttonx = None,  # button X
        self.buttony = c.display_height - 140,  # button Y
        super().__init__()
        self.shortname = 'a2',
        self.displayname = 'Archer Tower',
        self.level = '2'


class archertower3(Tower):
    def __init__(self, x, y):
        self.image = pygame.image.load('Resources/Towers/archer-tower3.png')
        self.rotate = False
        self.selected = False
        self.projectile = projectile.arrow
        self.projectilespeed = 17
        self.range = 200
        self.damage = 35
        self.attacks = 1
        self.speed = 600
        self.aoe = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 350
        self.upgradeprice = 500
        self.buttonx = None,  # button X
        self.buttony = c.display_height - 140,  # button Y
        super().__init__()
        self.shortname = 'a3',
        self.displayname = 'Archer Tower',
        self.level = '3'


class archertower4(Tower):
    def __init__(self, x, y):
        self.image = pygame.image.load('Resources/Towers/archer-tower3.png')
        self.rotate = False
        self.selected = False
        self.projectile = projectile.arrow
        self.projectilespeed = 20
        self.range = 225
        self.damage = 40
        self.attacks = 1
        self.speed = 800
        self.aoe = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 850
        self.upgradeprice = 2000
        self.buttonx = None,  # button X
        self.buttony = c.display_height - 140,  # button Y
        super().__init__()
        self.shortname = 'a4',
        self.displayname = 'Archer Tower',
        self.level = '4'

class archertower5(Tower):
    def __init__(self, x, y):
        self.image = pygame.image.load('Resources/Towers/archer-tower3.png')
        self.rotate = False
        self.selected = False
        self.projectile = projectile.arrow
        self.projectilespeed = 20
        self.range = 250
        self.damage = 40
        self.attacks = 1
        self.speed = 800
        self.aoe = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 2850
        self.upgradeprice = None
        self.buttonx = None,  # button X
        self.buttony = c.display_height - 140,  # button Y
        super().__init__()
        self.shortname = 'a5',
        self.displayname = 'Archer Tower',
        self.level = '5'


class ballistatower1(Tower):
    def __init__(self, x, y):
        self.image = pygame.image.load('Resources/Towers/ballista1.png')
        self.image2 = pygame.image.load('Resources/Towers/ballista1fired.png')
        self.rotate = True
        self.selected = False
        self.projectile = projectile.ballistaarrow
        self.projectilespeed = 22
        self.range = 250
        self.damage = 300
        self.attacks = 1
        self.speed = 20
        self.aoe = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 800
        self.upgradeprice = 800
        self.buttonx = 680,  # button X
        self.buttony = c.display_height - 140,  # button Y
        super().__init__()
        self.shortname = 'b1',
        self.displayname = 'Ballista Tower',
        self.level = '1'


class ballistatower2(Tower):
    def __init__(self, x, y):
        self.image = pygame.image.load('Resources/Towers/ballista1.png')
        self.image2 = pygame.image.load('Resources/Towers/ballista1fired.png')
        self.rotate = True
        self.selected = False
        self.projectile = projectile.ballistaarrow
        self.projectilespeed = 22
        self.range = 275
        self.damage = 375
        self.attacks = 1
        self.speed = 20
        self.aoe = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 1600
        self.upgradeprice = 1600
        self.buttonx = None,
        self.buttony = None,
        super().__init__()
        self.shortname = 'b2',
        self.displayname = 'Ballista Tower',
        self.level = '2'


class ballistatower3(Tower):
    def __init__(self, x, y):
        self.image = pygame.image.load('Resources/Towers/ballista3.png')
        self.image2 = pygame.image.load('Resources/Towers/ballista1fired.png')
        self.rotate = True
        self.selected = False
        self.projectile = projectile.ballistaarrow3
        self.projectilespeed = 23
        self.range = 300
        self.damage = 500
        self.attacks = 1
        self.speed = 20
        self.aoe = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 3200
        self.upgradeprice = 3200
        self.buttonx = None,
        self.buttony = None,
        super().__init__()
        self.shortname = 'b3',
        self.displayname = 'Ballista Tower',
        self.level = '3'


class ballistatower4(Tower):
    def __init__(self, x, y):
        self.image = pygame.image.load('Resources/Towers/ballista4.png')
        self.image2 = pygame.image.load('Resources/Towers/ballista4fired.png')
        self.rotate = True
        self.selected = False
        self.projectile = projectile.ballistaarrow4
        self.projectilespeed = 24
        self.range = 350
        self.damage = 600
        self.attacks = 1
        self.speed = 20
        self.aoe = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 6400
        self.upgradeprice = 6400
        self.buttonx = None,
        self.buttony = None,
        super().__init__()
        self.shortname = 'b4',
        self.displayname = 'Ballista Tower',
        self.level = '4'


class ballistatower5(Tower):
    def __init__(self, x, y):
        self.image = pygame.image.load('Resources/Towers/ballista5.png')
        self.image2 = pygame.image.load('Resources/Towers/ballista5fired.png')
        self.rotate = True
        self.selected = False
        self.projectile = projectile.ballistaarrow5
        self.projectilespeed = 25
        self.range = 400
        self.damage = 1000
        self.attacks = 1
        self.speed = 20
        self.aoe = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 12800
        self.upgradeprice = None
        self.buttonx = None,
        self.buttony = None,
        super().__init__()
        self.shortname = 'b5',
        self.displayname = 'Ballista Tower',
        self.level = '5'

def checkselected(tower):
    if tower.selected:
        return True
    else:
        return False


def getx(tower):
    print (tower.x / 40)
    return int(tower.x / 40)


def gety(tower):
    print(tower.y / 40)
    return int(tower.y / 40)


def checkprice(tower):
    return tower.price


def checkupgradeprice(tower):
    return tower.upgradeprice


basetowers = []
towers = []


def placetower(tower, x, y):
    stats.stats.gold -= tower.price
    placedtowers.add(tower.realtower(x * 40, y * 40))
    Map.changemap(tower.name, x, y)


"""
def displaytower(shortname, x, y):
    jawn = ""
    thelist = list(shortname)
    if thelist[0] == "a":
        if thelist[1] == "1":
            jawn = archertower1
        elif thelist[1] == "2":
            jawn = archertower2
    c.gameDisplay.blit(pygame.image.load(jawn.img1), (x * 40 - 1, y * 40 - 1))
"""

def upgradename(tower):
    oldname = list(tower.name)
    newnum = int(oldname[1]) + 1
    newname = str(oldname[0]) + str(newnum)
    return newname


def canplace(pos):
    y = t.listy(pos)
    x = t.listx(pos)
    if x <= 30:
        if y <= 14:
            if c.debugmap:
                print('x =' + str(x) + '  y =' + str(y) + '  ' + Map.map.map[y][x])
            if Map.map.map[y][x] == '- ':
                return True
            else:
                return False
    else:
        return False



