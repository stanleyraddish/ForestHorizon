import pygame

class Player(object):
    up, down, left, right = (0,-1), (0, 1), (-1, 0), (1,0)
    def __init__(self, x, y, width, height, boardX, boardY):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.speed = 4
        self.hitbox = pygame.Rect(self.x,self.y,self.width,self.height)
        self.direc = (1,0)
        self.tempPlayer = self.player
        self.boardX, self.boardY = boardX, boardY
        self.hp = 1000
        self.maxhp = 1000
        self.hpRatio = self.hp/self.maxhp
        self.isDead = False
        self.left = False
        self.isShoot = False

    def draw(self, win):
        gLen = 5*self.hpRatio*self.width/6
        pygame.draw.rect(win, (255,0,0), (self.x, self.y - self.height/7, 5*self.width/6, self.height/7))
        if self.hp > 0:
            pygame.draw.rect(win, (0,255,0), (self.x, self.y - self.height/7, gLen, self.height/7))
        win.blit(self.tempPlayer, (self.x, self.y))
        
    def update(self):
        if self.left == False:
            self.tempPlayer = self.player
        if self.left == True:
            self.tempPlayer = pygame.transform.flip(self.player, 1, 0)
        if self.x < 0:
            self.x = 0
        if self.x + self.width > self.boardX:
            self.x = self.boardX - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > self.boardY:
            self.y = self.boardY - self.height
        self.hitbox = pygame.Rect(self.x,self.y,self.width,self.height)
        if self.hp > self.maxhp:
            self.hp = self.maxhp
        self.hpRatio = self.hp/self.maxhp
        if self.hp < 0:
            self.hpRatio = 0
            self.isDead = True

    def move(self, rocks, direction):
        if direction == 'up':
            self.direc = Player.up
        if direction == 'down':
            self.direc = Player.down
        if direction == 'left':
            self.direc = Player.left
        if direction == 'right':
            self.direc = Player.right
        dx, dy = self.direc
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.hitbox = pygame.Rect(self.x,self.y,self.width,self.height)
        for rock in rocks:
            if rock.hitbox.colliderect(self.hitbox):
                self.x -= dx * self.speed
                self.y -= dy * self.speed