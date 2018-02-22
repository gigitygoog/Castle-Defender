import pygame
import stats
import Map
import tools as t
import constants as c
import HUD




zenemies = pygame.sprite.Group()


class enemyclass(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.x = -50
        self.rect.y = c.Spawny
        self.path = 'right'
        self.speed = 2
        self.selected = False
        if c.debugspawn:
            print("created a new sprite:", id(self))

    def update(self):
        if c.debugpath:
            print ("Moving")
        if self.selected:
            if HUD.hudvars.selectedenemyid != str(id(self)):
                self.selected = False
            else:
                HUD.hudvars.selectedenemy = self
        if self.health < 1:
            stats.stats.gold += self.bounty
            pygame.sprite.Sprite.kill(self)

        self.rect.move_ip((self.getdirection(self.rect.x, self.rect.y, self.speed, self.path)))
        if self.health > 0:
            self.hpbar()

    def hpbar(self):
        t.drawrec(self.rect.x + 5, self.rect.y, (self.health / self.basehealth) * 30, 3, c.RED)
        t.drawrec(self.rect.x + 5, self.rect.y, 30, 1, c.BLACK)
        t.drawrec(self.rect.x + 5, self.rect.y + 3, 30, 1, c.BLACK)
        t.drawrec(self.rect.x + 35, self.rect.y, 1, 3, c.BLACK)
        t.drawrec(self.rect.x + 4, self.rect.y, 1, 3, c.BLACK)

    def clickcheck(self, pos):
        if self.selected:
            self.selected = False
        if self.rect.collidepoint(pos):
            self.selected = True
            HUD.hudvars.selectedenemyid = str(id(self))
        else:
            pass

    def getdirection(self, x, y, speed, path):
        ym = int(y / 40)
        xm = int(x / 40)
        if c.debugpath:
            print("Checking: " + str(ym) + " " + str(xm))
            print(str(y / 40) + " " + str(int(y / 40)))
        if xm < 0:
            return speed, 0
        elif xm > 29:  # hit castle
            if c.debugpath:
                print ("REMOVED")
            stats.stats.castlehealth -= 1
            pygame.sprite.Sprite.kill(self)
            return 0, 0
        elif Map.map.map[ym][xm + 1] == "# " and (y / 40) == ym and path != 'left':  # Go right
            if c.debugpath:
                print("Going right!" + str(x) + " " + str(y))
            self.path = 'right'
            return speed, 0
        elif Map.map.map[ym - 1][xm] == "# " and (x / 40) == xm and path != 'down':  # Go up
            if c.debugpath:
                print("Going up!")
            self.path = 'up'
            return 0, -speed
        elif Map.map.map[ym][xm] == "# " and (y / 40) != ym and path != 'down':
            if c.debugpath:
                print("Going up to top!")
            self.path = 'up'
            return 0, -speed
        elif Map.map.map[ym + 1][xm] == "# " and (x / 40) == xm and path != 'up':  # Go up
            if c.debugpath:
                print("Going down!")
            self.path = 'down'
            return 0, speed
        elif Map.map.map[ym][xm - 1] == "# " and (y / 40) == ym and path != 'right':  # Go right
            if c.debugpath:
                print("Going left!" + str(x) + " " + str(y))
            self.path = 'left'
            return -speed, 0
        elif Map.map.map[ym][xm] == "# " and (x / 40) != xm and path != 'right':  # Go right
            if c.debugpath:
                print("Going all the way left!" + str(x) + " " + str(y))
            self.path = 'left'
            return -speed, 0

        else:
            print ("Something weird happened")

class barbarian1(enemyclass):
    def __init__(self):
        self.image = pygame.image.load('Resources/Enemies/ghsmile.png')
        self.imagelink = 'Resources/Enemies/ghsmile.png'
        super().__init__()
        self.displayname = "Barbarian"
        self.level = 1
        self.health = 50
        self.basehealth = self.health
        self.bounty = 10


class barbarian2(enemyclass):
    def __init__(self):
        self.image = pygame.image.load('Resources/Enemies/ghsmile2.png')
        self.imagelink = 'Resources/Enemies/ghsmile2.png'
        super().__init__()
        self.displayname = "Barbarian"
        self.health = 100
        self.basehealth = self.health
        self.level = 2
        self.bounty = 15


class barbarian3(enemyclass):
    def __init__(self):
        self.image = pygame.image.load('Resources/Enemies/ghsmile2.png')
        self.imagelink = 'Resources/Enemies/ghsmile2.png'
        super().__init__()
        self.displayname = "Barbarian"
        self.health = 175
        self.basehealth = self.health
        self.level = 3
        self.bounty = 20


class barbarian4(enemyclass):
    def __init__(self):
        self.image = pygame.image.load('Resources/Enemies/ghsmile2.png')
        self.imagelink = 'Resources/Enemies/ghsmile2.png'
        super().__init__()
        self.displayname = "Barbarian"
        self.health = 305
        self.basehealth = self.health
        self.level = 4
        self.bounty = 25

class barbarian5(enemyclass):
    def __init__(self):
        self.image = pygame.image.load('Resources/Enemies/ghsmile2.png')
        self.imagelink = 'Resources/Enemies/ghsmile2.png'
        super().__init__()
        self.displayname = "Barbarian"
        self.health = 500
        self.basehealth = self.health
        self.level = 5
        self.bounty = 30

class barbarian6(enemyclass):
    def __init__(self):
        self.image = pygame.image.load('Resources/Enemies/ghsmile2.png')
        self.imagelink = 'Resources/Enemies/ghsmile2.png'
        super().__init__()
        self.displayname = "Barbarian"
        self.health = 700
        self.basehealth = self.health
        self.level = 6
        self.bounty = 40

class barbarian7(enemyclass):
    def __init__(self):
        self.image = pygame.image.load('Resources/Enemies/ghsmile2.png')
        self.imagelink = 'Resources/Enemies/ghsmile2.png'
        super().__init__()
        self.displayname = "Barbarian"
        self.health = 1200
        self.basehealth = self.health
        self.level = 7
        self.bounty = 50

class barbarian8(enemyclass):
    def __init__(self):
        self.image = pygame.image.load('Resources/Enemies/ghsmile2.png')
        self.imagelink = 'Resources/Enemies/ghsmile2.png'
        super().__init__()
        self.displayname = "Barbarian"
        self.health = 1600
        self.basehealth = self.health
        self.level = 8
        self.bounty = 60

class barbarian9(enemyclass):
    def __init__(self):
        self.image = pygame.image.load('Resources/Enemies/ghsmile2.png')
        self.imagelink = 'Resources/Enemies/ghsmile2.png'
        super().__init__()
        self.displayname = "Barbarian"
        self.health = 2200
        self.basehealth = self.health
        self.level = 9
        self.bounty = 70

class barbarian10(enemyclass):
    def __init__(self):
        self.image = pygame.image.load('Resources/Enemies/ghsmile2.png')
        self.imagelink = 'Resources/Enemies/ghsmile2.png'
        super().__init__()
        self.displayname = "Barbarian"
        self.health = 2800
        self.basehealth = self.health
        self.level = 10
        self.bounty = 80


class barbarian11(enemyclass):
    def __init__(self):
        self.image = pygame.image.load('Resources/Enemies/ghsmile2.png')
        self.imagelink = 'Resources/Enemies/ghsmile2.png'
        super().__init__()
        self.displayname = "Barbarian"
        self.health = 3500
        self.basehealth = self.health
        self.level = 11
        self.bounty = 100


class barbarian12(enemyclass):
    def __init__(self):
        self.image = pygame.image.load('Resources/Enemies/ghsmile2.png')
        self.imagelink = 'Resources/Enemies/ghsmile2.png'
        super().__init__()
        self.displayname = "Barbarian"
        self.health = 5000
        self.basehealth = self.health
        self.level = 12
        self.bounty = 120


class barbarian13(enemyclass):
    def __init__(self):
        self.image = pygame.image.load('Resources/Enemies/ghsmile2.png')
        self.imagelink = 'Resources/Enemies/ghsmile2.png'
        super().__init__()
        self.displayname = "Barbarian"
        self.health = 7000
        self.basehealth = self.health
        self.level = 13
        self.bounty = 140

class barbarian14(enemyclass):
    def __init__(self):
        self.image = pygame.image.load('Resources/Enemies/ghsmile2.png')
        self.imagelink = 'Resources/Enemies/ghsmile2.png'
        super().__init__()
        self.displayname = "Barbarian"
        self.health = 9000
        self.basehealth = self.health
        self.level = 14
        self.bounty = 160

class barbarian15(enemyclass):
    def __init__(self):
        self.image = pygame.image.load('Resources/Enemies/ghsmile2.png')
        self.imagelink = 'Resources/Enemies/ghsmile2.png'
        super().__init__()
        self.displayname = "Barbarian"
        self.health = 12000
        self.basehealth = self.health
        self.level = 15
        self.bounty = 180



