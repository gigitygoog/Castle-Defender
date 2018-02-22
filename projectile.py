import pygame
import math
import constants as c
projectiles = pygame.sprite.Group()


class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle = self.getangle()
        self.image = pygame.transform.rotate(self.image, self.angle)
        if c.debugtargeting:
            print ("Sent at angle:" + str(self.angle))
    def update(self):
       # print ("My actual angle is:" + str(self.angle))
        if abs(self.rect.x - self.target.rect.x) < 20 and abs(self.rect.y - self.target.rect.y) < 40:
            if self.target.health > 0:
                self.hit()
            else:
                self.kill()
        if self.target.health > 0:
            self.angle = self.getangle()
        self.rect.move_ip((self.getmove()))
        #self.rect.move_ip((1, 1))
        #print("My location is " + str(self.rect.x) + "  " + str(self.rect.y))
      #  print(str(math.degrees(math.sin(math.radians(30))) * 15))

    def getmove(self): # x and y values to change to go to target at set angle
        hypotenuse = self.speed
        angle = self.angle

        if self.angle == 0: # Straight up
            return 0, -self.speed

        elif self.angle == 90: # Straight left
            return -self.speed, 0

        elif self.angle == 180: # Straight Down
            return 0, self.speed

        elif self.angle == -90: # Straight right
            return self.speed, 0

        elif self.angle > 0 and self.angle < 90: # Top left
            realangle = 90 - abs(angle)
            opposite = (math.sin(math.radians(realangle))) * hypotenuse
            adjacent = (hypotenuse ** 2 - opposite ** 2) ** (1 / 2)
           # print (str(adjacent) + " "  + str(opposite))
          #  print ("Moving x: " + str(-adjacent) + "   y:" + str(-opposite) )
            return -adjacent, -opposite

        elif self.angle > 90 and self.angle < 180: # Bottom Left
            realangle = abs(angle) - 90
            opposite = (math.sin(math.radians(realangle))) * hypotenuse
            adjacent = (hypotenuse ** 2 - opposite ** 2) ** (1 / 2)
           # print (str(adjacent) + " "  + str(opposite))
            return -adjacent, opposite

        elif self.angle < 0 and self.angle > -90: # Top Right
            realangle = 90 - abs(angle)
            opposite = (math.sin(math.radians(realangle))) * hypotenuse
            adjacent = (hypotenuse ** 2 - opposite ** 2) ** (1 / 2)
         #   print (str(adjacent) + " "  + str(opposite))
            return adjacent, -opposite

        elif -180 < self.angle < -90: # Bottom Right
            realangle = abs(angle) - 90
            opposite = (math.sin(math.radians(realangle))) * hypotenuse
            adjacent = (hypotenuse ** 2 - opposite ** 2) ** (1/2)
          #  print (str(adjacent) + " "  + str(opposite))
         #   print (str(realangle))
            return adjacent, opposite

    def getangle(self): # Angle to launch at and rotate
        if (self.rect.y == self.target.rect.y or abs(self.rect.y - self.target.rect.y) < 15) and self.rect.x > self.target.rect.x: # Straight Left
            if c.debugtargeting:
                print ("Target has the same y as me. Going Left!")
            return 90

        elif (self.rect.x == self.target.rect.x or abs(self.rect.x - self.target.rect.x)) < 15 and self.rect.y > self.target.rect.y: # Straight Up
            if c.debugtargeting:
                print ("Target has same x as me. Going up!")
            return 0

        elif (self.rect.y == self.target.rect.y or abs(self.rect.y - self.target.rect.y) < 15) and self.rect.x < self.target.rect.x: # Straight Right
            if c.debugtargeting:
                print ("Target has the same y as me. Going Right!")
            return -90

        elif (self.rect.x == self.target.rect.x or abs(self.rect.x - self.target.rect.x) < 15) and self.rect.y < self.target.rect.y: # Straight Down
            if c.debugtargeting:
                print ("Target has same x as me. Going Down!")
            return 180

        elif self.rect.x - self.target.rect.x > 0 and self.rect.y - self.target.rect.y >= 0: #Top left triangle
            if c.debugtargeting:
                print ("I am trying top left triangle: " + str(self.rect.x) + " " + str(self.rect.y) + " " + str(self.target.rect.x) + " " + str(self.target.rect.y))

            adjacent = abs(self.rect.x - self.target.rect.x)
            opposite = abs(self.rect.y - self.target.rect.y)
            hypotenuse = (adjacent ** 2 + opposite ** 2) ** (1/2.0)
            if c.debugtargeting:
                print ("Opposite: " + str(opposite))
                print ("Adjacent: " + str(adjacent))
            return 90 - math.degrees(math.atan(opposite / adjacent))

        elif self.target.rect.x - self.rect.x > 0 and self.rect.y - self.target.rect.y >= 0: #Top right triangle
            if c.debugtargeting:
                print ("I am trying top right triangle: " + str(self.rect.x) + " " + str(self.rect.y) + " " + str(self.target.rect.x) + " " + str(self.target.rect.y))
            adjacent = abs(self.rect.x - self.target.rect.x)
            opposite = abs(self.rect.y - self.target.rect.y)
            hypotenuse = (adjacent ** 2 + opposite ** 2) ** (1/2.0)
          #  print ("The angle is " + str(math.degrees(math.atan(tan))))
           # return -90 + math.degrees(math.acos(adjacent / hypotenuse))
            return -90 + math.degrees(math.atan(opposite / adjacent))

        elif self.target.rect.x - self.rect.x > 0 and self.target.rect.y - self.target.rect.y >= 0: #Bottom Right triangle
            if c.debugtargeting:
                print ("I am trying Bottom Right triangle: " + str(self.rect.x) + " " + str(self.rect.y) + " " + str(self.target.rect.x) + " " + str(self.target.rect.y))
            adjacent = abs(self.rect.x - self.target.rect.x)
            opposite = abs(self.rect.y - self.target.rect.y)
            hypotenuse = (adjacent ** 2 + opposite ** 2) ** (1/2.0)
          #  print ("The angle is " + str(math.degrees(math.atan(tan))))
           # return -90 + -math.degrees(math.acos(adjacent / hypotenuse))
            return -90 - math.degrees(math.atan(opposite / adjacent))

        elif self.rect.x - self.target.rect.x > 0 and self.target.rect.y - self.target.rect.y >= 0: #Bottom left triangle
            if c.debugtargeting:
                print ("I am trying Bottom left triangle: " + str(self.rect.x) + " " + str(self.rect.y) + " " + str(self.target.rect.x) + " " + str(self.target.rect.y))
            adjacent = abs(self.rect.x - self.target.rect.x)
            opposite = abs(self.rect.y - self.target.rect.y)
            hypotenuse = (adjacent ** 2 + opposite ** 2) ** (1/2.0)
          #  print ("The angle is " + str(math.degrees(math.acos(cos))))
            #return 90 + math.degrees(math.acos(adjacent / hypotenuse))
            return 90 + math.degrees(math.atan(opposite / adjacent))

        elif self.rect.x == self.target.rect.x and self.target.rect.y == self.rect.y:
            if c.debugtargeting:
                print("me =" + str(self.rect.x) + "  " + str(self.rect.y))
                print("Them =" + str(self.target.rect.x) + "  " + str(self.target.rect.y ))
            return 0

        else:
            if c.debugtargeting:
                print ("Error with targeting projectile.py line 135")
                print("me =" + str(self.rect.x) + "  " + str(self.rect.y))
                print("Them =" + str(self.target.rect.x) + "  " + str(self.target.rect.y ))

    def hit(self):
        if c.debugtargeting:
            print ("I hit it!")
            print (str(self.rect.x) + str(self.rect.y))
        self.target.health -= self.basedamage
        pygame.sprite.Sprite.kill(self)

class arrow(Projectile):
    def __init__(self, startx, starty, target, base, speed):
        self.image = pygame.image.load('Resources/Projectiles/arrow1.png')
        self.rect = self.image.get_rect()
        self.target = target
        self.speed = speed
        self.basedamage = base
        self.rect.x = startx
        self.rect.y = starty
        self.basetargetx = startx
        self.basetargety = starty

        super().__init__()


class ballistaarrow(Projectile):
    def __init__(self, startx, starty, target, base, speed):
        self.image = pygame.image.load('Resources/Projectiles/ballistaarrow1.png')
        self.rect = self.image.get_rect()
        self.target = target
        self.speed = speed
        self.basedamage = base
        self.rect.x = startx
        self.rect.y = starty
        self.basetargetx = startx
        self.basetargety = starty

        super().__init__()

class ballistaarrow3(Projectile):
    def __init__(self, startx, starty, target, base, speed):
        self.image = pygame.image.load('Resources/Projectiles/ballistaarrow3.png')
        self.rect = self.image.get_rect()
        self.target = target
        self.speed = speed
        self.basedamage = base
        self.rect.x = startx
        self.rect.y = starty
        self.basetargetx = startx
        self.basetargety = starty

        super().__init__()

class ballistaarrow4(Projectile):
    def __init__(self, startx, starty, target, base, speed):
        self.image = pygame.image.load('Resources/Projectiles/ballistaarrow4.png')
        self.rect = self.image.get_rect()
        self.target = target
        self.speed = speed
        self.basedamage = base
        self.rect.x = startx
        self.rect.y = starty
        self.basetargetx = startx
        self.basetargety = starty

        super().__init__()


class ballistaarrow5(Projectile):
    def __init__(self, startx, starty, target, base, speed):
        self.image = pygame.image.load('Resources/Projectiles/ballistaarrow5.png')
        self.rect = self.image.get_rect()
        self.target = target
        self.speed = speed
        self.basedamage = base
        self.rect.x = startx
        self.rect.y = starty
        self.basetargetx = startx
        self.basetargety = starty

        super().__init__()