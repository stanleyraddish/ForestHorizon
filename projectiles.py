from functions import Functions
import pygame
import math
from spriteSheets import SpriteSheet
class RegBullet(object):
    # Image from Pixel Art
    # http://pixelartmaker.com/gallery?after=568768
    def __init__(self, x, y, width, height, vX, vY, speed, angle):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.vX, self.vY = vX, vY
        self.speed = speed
        regBullet = pygame.image.load('regbullet.png').convert_alpha()
        regBullet = pygame.transform.scale(regBullet, (width, height))
        regBullet = pygame.transform.rotate(regBullet, angle)
        self.image = regBullet
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.damage = 25
    def draw(self, win):
        #pygame.draw.rect(win, (0,255,0), self.hitbox)
        win.blit(self.image,(self.x, self.y))
    def update(self):
        self.x += self.vX * self.speed
        self.y += self.vY * self.speed
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

class GunnerUltBullet(RegBullet):
    # Image from chrismalnu.wordpress.com
    # https://chrismalnu.wordpress.com/category/shoot-em-up/
    def __init__(self, x, y, width, height, vX, vY, speed, angle):
        super().__init__(x, y, width, height, vX, vY, speed, angle)
        ultBullet = pygame.image.load('gunnerultbullet.png').convert_alpha()
        ultBullet = pygame.transform.scale(ultBullet, (width, height))
        ultBullet = pygame.transform.rotate(ultBullet, angle)
        self.image = ultBullet
        self.damage = 30

class GunnerQBullet(RegBullet):
    # Image from pngriver
    # https://pngriver.com/download-light-png-clipart-1-82708/
    def __init__(self, x, y, width, height, vX, vY, speed, angle, detX, detY, main = True):
        super().__init__(x, y, width, height, vX, vY, speed, angle)
        qBullet = pygame.image.load('gunnerQ.png').convert_alpha()
        qBullet = pygame.transform.scale(qBullet, (width, height))
        qBullet = pygame.transform.rotate(qBullet, angle)
        self.angle = angle
        self.image = qBullet
        self.damage = 45
        self.tempImg = self.image
        self.detX, self.detY = detX, detY
        self.isDet = False
        self.isMain = main
    def update(self):
        super().update()
        self.angle += 40
        if self.checkDet():
            self.isDet = True
        self.tempImg = pygame.transform.rotate(self.image, self.angle)
    def draw(self, win):
        win.blit(self.tempImg,(self.x, self.y))
    def checkDet(self):
        if self.x < self.detX + 5 and self.x > self.detX - 5 and self.y < self.detY + 5 and self.y > self.detY - 5:
            return True
        return False

class WizBullet(RegBullet):
    # image sprite from: https://ya-webdesign.com/image/light-orb-png/732681.html
    def __init__(self, x, y, width, height, vX, vY, speed, angle):
        super().__init__(x, y, width, height, vX, vY, speed, angle)
        wizBullet = pygame.image.load('bolt2.png').convert_alpha()
        wizBullet = pygame.transform.scale(wizBullet, (width, height))
        wizBullet = pygame.transform.rotate(wizBullet, angle)
        self.image = wizBullet
        self.damage = 15
        self.tempImg = self.image
        self.angle = angle
        self.target = None
    def draw(self, win):
        win.blit(self.tempImg, (self.x, self.y))
    def update(self):
        if self.target != None:
            self.vX, self.vY = Functions.rotary(self.vX, self.vY, self.target.x - self.x, self.target.y - self.y, 0.04)
        self.angle = Functions.getRotation(0, self.vX, self.vY)
        self.x += self.vX * self.speed
        self.y += self.vY * self.speed
        self.tempImg = pygame.transform.rotate(self.image, self.angle)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

class FrostOrb(object):
    def __init__(self, cx, cy, angle, width, height):
        self.x, self.y = 400, 400
        self.cx, self.cy = cx, cy
        self.width, self.height = width, height
        self.angleC = angle #from center of spell
        self.angleS = 0 #from self center
        orb = pygame.image.load('boltt.png').convert_alpha()
        orb = pygame.transform.scale(orb, (width, height))
        self.image = orb
        self.hitbox = self.image.get_rect()
        self.damage = 0.3
        self.tempImg = self.image
        self.rect = self.image.get_rect()
    def draw(self, win):
        win.blit(self.tempImg,self.hitbox)
    def update(self):
        self.angleS += 0.4
        self.angleC += 1.5
        self.x = self.cx + 200 * math.cos(self.angleC * math.pi/180)
        self.y = self.cy + 200 * math.sin(self.angleC * math.pi/180)
        self.hitbox.center = (self.x, self.y)
        self.tempImg = pygame.transform.rotate(self.image, self.angleS)

class GunnerBarrel(object):
    # sprite from https://www.pinterest.com/pin/496521927642314806/
    def __init__(self, x, y, width, height, number, target = False):
        self.x, self.y = x, y
        barrel = pygame.image.load('barrel.png').convert_alpha()
        barrel = pygame.transform.scale(barrel, (width, height))
        self.image = barrel
        self.hitbox = self.image.get_rect()
        self.hitbox.center = (self.x, self.y)
        self.number = number * 100
        self.f = pygame.font.Font(None, 30)
        self.t = self.f.render(f'{self.number//100}', True, (0,0,0))
        self.tRect = self.t.get_rect()
        self.tRect.center = (self.x, self.y + 5*height/8)
        self.height = height
    
    def update(self):
        self.number -= 1
    def draw(self, win):
        color = (0,0,0)
        t = self.f.render(f'{self.number//100 + 1}', True, color)
        win.blit(self.image, self.hitbox)
        win.blit(t, self.tRect)

class BarrelExplosion(object):
    # sprite sheet from https://www.seekpng.com/ipng/u2q8t4i1o0t4a9u2_drawn-explosions-sprite-explosion-sprite-sheet-doom/
    def __init__(self, x, y, width, height):
        self.expSheet = SpriteSheet("barexpsprites.png", 8, 6, 48, width, height)
        self.frame = 0
        self.hitbox = pygame.Rect(0,0,width,height)
        self.hitbox.center = (x,y)
        self.x, self.y = x,y
        self.damage = 90
    
    def draw(self, win):
        self.expSheet.draw(win, self.frame, self.x, self.y, 1)

    def update(self):
        self.frame += 1

    
class Rock(object):
    # sprite from https://ya-webdesign.com/image/rock-sprite-png/850113.html
    def __init__(self, x, y, image, size):
        self.image = image
        self.size = size
        self.x, self.y = x, y
        self.hitbox = pygame.Rect(0,0,11*self.size//16, self.size//2)
        self.hitbox.center = self.x, self.y + self.size //20

    def draw(self, win):
        pygame.draw.rect(win,(0,0,0), self.hitbox)
        win.blit(self.image, (self.x - self.size//2, self.y - 3* self.size//8))
    
    @staticmethod
    def newRock(boardX, boardY, size):
        rock = pygame.image.load('rock.png').convert_alpha()
        rock = pygame.transform.scale(rock, (size, 3*size//4))
        x, y= Functions.randomPos2(boardX, boardY, size, size)
        return Rock(x, y, rock, size)
        



