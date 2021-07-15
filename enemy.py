import pygame
import random
from functions import Functions
import math
from spriteSheets import SpriteSheet

# sprite sheet for all birds from: https://www.pinterest.com/pin/440297301067856684/
class Enemy(object):
    def __init__(self, x, y, dim):
        self.spriteSheet = SpriteSheet('birds.png', 12, 8, 96, dim, dim)
        self.x, self.y = x, y
        self.dim = dim
        self.hitbox = pygame.Rect(self.x,self.y,self.dim,self.dim)
        self.direc = 'up'
        self.isSlow = False
        self.isSupSlow = False
        self.wizQTimer = 0
        self.canExp = True
        self.expTimer = 0
        self.flyFrame = 0
        self.index = 0
        self.direcDict = {'down': 0, 'left': 1, 'right': 2, 'up': 3}
        self.wingMotion = 'down'
        self.flapTimer = 0
        self.flapMod = 9
        # can change for birds
        self.normalFlapMod = 9
        self.birdNumb = 4
        self.sheetColOff, self.sheetRowOff = 3 * (self.birdNumb % 4), 4 * (self.birdNumb // 4)
        self.damage = 80
        self.normalSpeed = 3
        self.speed = 3
        self.maxhp = 100
        self.hp = 100
        self.hpRatio = self.hp/self.maxhp

    def draw(self,win):
        #pygame.draw.rect(win, (0,0,140), self.hitbox)
        gLen = 2*self.hpRatio*self.dim/3
        pygame.draw.rect(win, (255,0,0), (self.x + self.dim/6, self.y, 2*self.dim/3, self.dim/7))
        pygame.draw.rect(win, (0,255,0), (self.x + self.dim/6, self.y, gLen, self.dim/7))
        self.spriteSheet.draw(win, self.index, self.x, self.y, 0)

    def update(self, playerX, playerY, rocks):
        if self.canExp == False:
            self.expTimer -= 1
            if self.expTimer == 0:
                self.canExp = True
        if self.wizQTimer > 0:
            self.wizQTimer -= 1
            self.speed = 0
            self.flapMod = 9999999
        else:
            self.speed = self.normalSpeed
            self.flapMod = self.normalFlapMod
            if self.isSupSlow:
                self.speed = 0.8*self.normalSpeed/3
                #self.flapMod = 30
            elif self.isSlow:
                self.speed = 1.8*self.normalSpeed/3
                #self.flapMod = 22
        vec = Functions.unitVector((self.x, self.y), (playerX, playerY))
        self.x += vec[0] * self.speed
        self.hitbox = pygame.Rect(self.x,self.y,self.dim,self.dim)
        for rock in rocks:
            if rock.hitbox.colliderect(self.hitbox):
                self.x -= vec[0] * self.speed
        self.y += vec[1] * self.speed
        self.hitbox = pygame.Rect(self.x,self.y,self.dim,self.dim)
        for rock in rocks:
            if rock.hitbox.colliderect(self.hitbox):
                self.y -= vec[1] * self.speed
        angle = Functions.getRotation(0, *vec)
        if -135 <= angle < -45:
            self.direc = 'down'
        elif -45 <= angle < 45:
            self.direc = 'right'
        elif angle >= 45 or angle < -255:
            self.direc = 'up'
        elif -225 <= angle < 135:
            self.direc = 'left'
        self.hitbox = pygame.Rect(self.x,self.y,self.dim,self.dim)
        self.hpRatio = self.hp/self.maxhp
        self.flapTimer += 1
        if self.flapTimer % self.flapMod == 0:
            if self.wingMotion == 'up':
                if self.flyFrame == 1:
                    self.flyFrame = 0
                    self.wingMotion = 'down'
                elif self.flyFrame == 2:
                    self.flyFrame = 1
            elif self.wingMotion == 'down':
                if self.flyFrame == 1:
                    self.flyFrame = 2
                    self.wingMotion = 'up'
                elif self.flyFrame == 0:
                    self.flyFrame = 1
        indCol = self.flyFrame + self.sheetColOff
        indRow = self.direcDict[self.direc] + self.sheetRowOff
        self.index = 12 * indRow + indCol


    @staticmethod
    def newEnemy(boardX, boardY, size):
        x, y = Functions.randomPos(boardX, boardY, size, size)
        return Enemy(x, y, size)

class Enemy2(Enemy):
    def __init__(self, x, y, dim):
        super().__init__(x, y, dim)
        self.normalFlapMod = 5
        self.birdNumb = 2
        self.sheetColOff, self.sheetRowOff = 3 * (self.birdNumb % 4), 4 * (self.birdNumb // 4)
        self.damage = 70
        self.normalSpeed = 10
        self.maxhp = 20
        self.hp = 20
        self.hpRatio = self.hp/self.maxhp
    
    def newEnemy(boardX, boardY, size):
        x, y = Functions.randomPos(boardX, boardY, size, size)
        return Enemy2(x, y, size)

class Enemy3(Enemy):
    def __init__(self, x, y, dim):
        super().__init__(x, y, dim)
        self.normalFlapMod = 12
        self.birdNumb = 0
        self.sheetColOff, self.sheetRowOff = 3 * (self.birdNumb % 4), 4 * (self.birdNumb // 4)
        self.damage = 150
        self.normalSpeed = 1
        self.maxhp = 400
        self.hp = 400
        self.hpRatio = self.hp/self.maxhp
    
    def newEnemy(boardX, boardY, size):
        x, y = Functions.randomPos(boardX, boardY, size, size)
        return Enemy3(x, y, size)

class Enemy4(Enemy):
    def __init__(self, x, y, dim):
        super().__init__(x, y, dim)
        self.normalFlapMod = 15
        self.birdNumb = 6
        self.sheetColOff, self.sheetRowOff = 3 * (self.birdNumb % 4), 4 * (self.birdNumb // 4)
        self.damage = 100
        self.normalSpeed = 3
        self.maxhp = 150
        self.hp = 150
        self.hpRatio = self.hp/self.maxhp
    
    def newEnemy(boardX, boardY, size):
        x, y = Functions.randomPos(boardX, boardY, size, size)
        return Enemy4(x, y, size)
    
    def update(self, playerX, playerY, rocks):
        if self.canExp == False:
            self.expTimer -= 1
            if self.expTimer == 0:
                self.canExp = True
        if self.wizQTimer > 0:
            self.wizQTimer -= 1
            self.speed = 0
            self.flapMod = 9999999
        else:
            self.speed = self.normalSpeed
            self.flapMod = self.normalFlapMod
            if self.isSupSlow:
                self.speed = 0.8*self.normalSpeed/3
                #self.flapMod = 30
            elif self.isSlow:
                self.speed = 1.8*self.normalSpeed/3
                #self.flapMod = 22
        vec = Functions.unitVector((self.x, self.y), (playerX, playerY))
        closestRock = Functions.closestIn(self, rocks)
        if Functions.getDist(self, closestRock) < 130:
            rockangle = -Functions.getRotation(0, (closestRock.x - self.x), (closestRock.y - self.y)) % 360
            angle = -Functions.getRotation(0, *vec) % 360
            diff = angle - rockangle
            if -50 <= diff <= 0:
                angle = rockangle - 120
            elif 0 < diff < 50:
                angle = rockangle + 120
            angle *= math.pi/180
            x, y = math.cos(angle), math.sin(angle)
            vec = Functions.rotary(*vec, x, y, 0.7)
            vec = Functions.rotary(*vec, self.x - closestRock.x, self.y - closestRock.y,0.3)
        self.x += vec[0] * self.speed
        self.hitbox = pygame.Rect(self.x,self.y,self.dim,self.dim)
        for rock in rocks:
            if rock.hitbox.colliderect(self.hitbox):
                self.x -= vec[0] * self.speed
        self.y += vec[1] * self.speed
        self.hitbox = pygame.Rect(self.x,self.y,self.dim,self.dim)
        for rock in rocks:
            if rock.hitbox.colliderect(self.hitbox):
                self.y -= vec[1] * self.speed
        angle = Functions.getRotation(0, *vec)
        if -135 <= angle < -45:
            self.direc = 'down'
        elif -45 <= angle < 45:
            self.direc = 'right'
        elif angle >= 45 or angle < -255:
            self.direc = 'up'
        elif -225 <= angle < 135:
            self.direc = 'left'
        self.hitbox = pygame.Rect(self.x,self.y,self.dim,self.dim)
        self.hpRatio = self.hp/self.maxhp
        self.flapTimer += 1
        if self.flapTimer % self.flapMod == 0:
            if self.wingMotion == 'up':
                if self.flyFrame == 1:
                    self.flyFrame = 0
                    self.wingMotion = 'down'
                elif self.flyFrame == 2:
                    self.flyFrame = 1
            elif self.wingMotion == 'down':
                if self.flyFrame == 1:
                    self.flyFrame = 2
                    self.wingMotion = 'up'
                elif self.flyFrame == 0:
                    self.flyFrame = 1
        indCol = self.flyFrame + self.sheetColOff
        indRow = self.direcDict[self.direc] + self.sheetRowOff
        self.index = 12 * indRow + indCol



        
    