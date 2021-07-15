import pygame
from functions import Functions
class HealthPack(object):
    # sprite from https://opengameart.org/content/heart-pixel-art
    def __init__(self, boardX, boardY, rocks):
        self.dim = 50
        life = pygame.image.load('life.png').convert_alpha()
        life = pygame.transform.scale(life, (self.dim, self.dim))
        self.image = life
        valid = False
        while valid == False:
            self.center = Functions.randomPos2(boardX, boardY, 3*self.dim//2, 3*self.dim//2)
            self.hitbox = pygame.Rect(*self.center, self.dim, self.dim)
            self.hitbox.center = self.center
            works = True
            for rock in rocks:
                if rock.hitbox.colliderect(self.hitbox):
                    works = False
                    break   
            if works == True:    
                valid = True
        self.scale = 1
        self.scaleDir = 1
        self.tempImg = self.image
        self.healing = 150
        self.timer = 600
    
    def draw(self, win):
        win.blit(self.tempImg, self.center)
    
    def update(self):
        self.timer -=1
        if self.scaleDir == 1:
            self.scale += 0.02
            if self.scale >= 1.3:
                self.scaleDir = -1
        elif self.scaleDir == -1:
            self.scale -= 0.02
            if self.scale <= 0.7:
                self.scaleDir = 1
        self.tempImg = pygame.transform.rotozoom(self.image, 0, self.scale)
        if self.timer < 255:
            self.tempImg.set_alpha(self.timer)
            if (self.timer // 20) % 2 == 0:
                self.tempImg.set_alpha(3)
        self.hitbox = pygame.Rect(*self.center, self.dim*self.scale, self.dim*self.scale)
        self.hitbox.center = self.center

class Speed(HealthPack):
    #sprite from https://www.pinclipart.com/maxpin/iRoxwRR/
    def __init__(self, boardX, boardY, rocks):
        super().__init__(boardX, boardY, rocks)
        self.dim = 50
        speed = pygame.image.load('speed.png').convert_alpha()
        speed = pygame.transform.scale(speed, (self.dim, self.dim))
        self.image = speed
        valid = False
        while valid == False:
            self.center = Functions.randomPos2(boardX, boardY, 3*self.dim//2, 3*self.dim//2)
            self.hitbox = pygame.Rect(*self.center, self.dim, self.dim)
            self.hitbox.center = self.center
            works = True
            for rock in rocks:
                if rock.hitbox.colliderect(self.hitbox):
                    works = False
                    break   
            if works == True:    
                valid = True
        self.healing = 0
        self.timer = 800

