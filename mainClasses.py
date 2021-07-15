from projectiles import *
from functions import Functions
from player import Player
import math
import copy
from spriteSheets import SpriteSheet

class Gunner(Player):
    # Gunner Sprite from https://toppng.com/show_download/180720/avgn-adventures-avgn-sprite-8-bit-character/large
    player = pygame.image.load('player.png')
    desc = pygame.image.load('gunnerDesc.png')
    def __init__(self, x, y, width, height, boardX, boardY):
        super().__init__(x, y, width, height, boardX, boardY)
        self.player = pygame.image.load('player.png').convert_alpha()
        self.player = pygame.transform.scale(self.player, (width, height))
        self.bullets = []
        self.isUlt = False
        self.ultAmmo = 0
        self.maxUltAmmo = 300
        self.qAmmo = 250
        self.maxQAmmo = 250
        self.eAmmo = 100
        self.maxEAmmo = 100
        self.regenCounter = 0
        self.regenMax = 10
        self.maxhp = 700
        self.barrels = {1:None, 2:None, 3:None, 4:None}
        self.explosions = []
        self.shoot = 0
        self.shootRate = 30

    def clickSkill(self, mouseX, mouseY):
        if self.isUlt == False:
            y = self.y + 3*self.height/7
            if self.left == True:
                x = self.x - self.width / 7
            else:
                x = self.x + self.width - self.width/7
            vec = Functions.unitVector((x, y), (mouseX, mouseY))
            angle = Functions.getRotation(0, *vec)
            angle2 = -(angle - 6)
            angle3 = -(angle + 6)
            vec2 = (math.cos(angle2*math.pi/180), math.sin(angle2*math.pi/180))
            vec3 = (math.cos(angle3*math.pi/180), math.sin(angle3*math.pi/180))
            self.bullets.append(self.regBullet(x, y, *vec2, -angle2))
            self.bullets.append(self.regBullet(x, y, *vec3, -angle3))
    
    def startUlt(self):
        if self.ultAmmo == self.maxUltAmmo:
            self.isUlt = True

    def qSkill(self, mouseX, mouseY):
        if self.qAmmo == self.maxQAmmo:
            y = self.y + self.height/2
            if self.left == True:
                x = self.x - self.width / 7
            else:
                x = self.x + self.width - self.width/7
            vec = Functions.unitVector((x, y), (mouseX, mouseY))
            angle = Functions.getRotation(25, *vec)
            self.bullets.append(self.qBullet(x, y, *vec, angle, mouseX, mouseY))
            self.qAmmo = 0

    def regBullet(self, x, y, vX, vY, angle):
        return RegBullet(x, y, 20, 5, vX, vY, 7, angle)
    
    def ultBullet(self, x, y, vX, vY, angle):
        return GunnerUltBullet(x, y, 60, 40, vX, vY, 25, angle)
    
    def qBullet(self, x, y, vX, vY, angle, detX, detY):
        return GunnerQBullet(x, y, 20, 20, vX, vY, 10, angle, detX, detY)

    def qSplitBullets(self, x, y):
        buls = []
        ang = [n * 24 for n in range(15)]
        for angle in ang:
            angRad = angle * math.pi / 180
            vx, vy = math.cos(angRad), math.sin(angRad)
            buls.append(GunnerQBullet(x, y, 50, 50, vx, vy, 8, angle, -999, -999, False))
        return buls

    def LapisAndLazuli(self, mouseX, mouseY):
        y = self.y + self.height/4
        if self.left == True:
            x = self.x - self.width / 3
        else:
            x = self.x + self.width - self.width/6
        vec = Functions.unitVector((x, y), (mouseX, mouseY))
        angle = Functions.getRotation(180, *vec)
        if self.ultAmmo > 0:
            if self.ultAmmo % 6 == 0:
                self.bullets.append(self.ultBullet(x, y, *vec, angle))
            self.ultAmmo -= 1
        else:
            self.isUlt = False

    def draw1(self, win):
        for bullet in self.bullets:
            bullet.draw(win)  
        for barrelN in self.barrels:
            if self.barrels[barrelN] != None:
                self.barrels[barrelN].draw(win)
        for exp in self.explosions:
            exp.draw(win)

    def eSkill(self, mouseX, mouseY, rocks = None):
        if self.eAmmo == self.maxEAmmo:
            works = True
            temp = pygame.Rect(0,0,80,80)
            temp.center = mouseX, mouseY
            for rock in rocks:
                if rock.hitbox.colliderect(temp):
                    works = False
                    break
            if works:
                for i in range(1, 5):
                    if self.barrels[i] == None:
                        self.barrels[i] = GunnerBarrel(mouseX, mouseY, 80, 80, 3)
                        self.eAmmo = 0
                        break
    def detBarrel(self, x, y, barrelN):
        self.barrels[barrelN] = None
        self.explosions.append(BarrelExplosion(x, y, 250, 250))

    def update1(self, mouseX, mouseY, boardX, boardY):
        self.regenCounter += 1
        if self.regenCounter % self.regenMax == 0:
            self.hp += 1
        if self.qAmmo < self.maxQAmmo:
            self.qAmmo += 1
        if self.eAmmo < self.maxEAmmo:
            self.eAmmo += 1
        if self.isUlt == True:
            self.LapisAndLazuli(mouseX, mouseY)
        elif self.ultAmmo >= self.maxUltAmmo:
            self.ultAmmo = self.maxUltAmmo
        for bullet in self.bullets:
            if bullet.x > boardX + bullet.width  or bullet.x < - bullet.width:
                self.bullets.remove(bullet)
            elif bullet.y > boardY + bullet.height  or bullet.y < - bullet.height:
                self.bullets.remove(bullet)
        tempbullets = copy.copy(self.bullets)
        for bullet in tempbullets:
            bullet.update()
            if isinstance(bullet, GunnerQBullet):
                if bullet.isDet:
                    for bul in self.qSplitBullets(bullet.x, bullet.y):
                        self.bullets.append(bul)
        for barrelN in self.barrels:
            if self.barrels[barrelN] != None:
                bar = self.barrels[barrelN]
                bar.update()
                if bar.number == 0:
                    self.detBarrel(bar.x, bar.y, barrelN)
        tempExp = self.explosions
        for exp in tempExp:
            exp.update()
            if exp.frame >= 48:
                self.explosions.remove(exp)
        if self.isShoot and (self.shoot % self.shootRate == 0 or self.shoot % self.shootRate == 8):
            self.clickSkill(mouseX, mouseY)
        self.shoot += 1
                   
        
class Wizard(Player):
    # Q Skill Sprite Sheet from http://rosprites.blogspot.com/2013/09/spell-effects-more.html
    # E Skill Teleport Effect Spirte Sheet from https://opengameart.org/content/animated-particle-effects-2
    # Wizard Sprite from https://opengameart.org/content/animated-particle-effects-2
    player = pygame.image.load('wiz.png')
    desc = pygame.image.load('wizDesc.png')
    def __init__(self, x, y, width, height, boardX, boardY):
        super().__init__(x, y, width, height, boardX, boardY)
        self.bullets = []
        self.isUlt = False
        self.ultAmmo = 0
        self.maxUltAmmo = 240
        self.qAmmo = 130
        self.maxQAmmo = 130
        self.eAmmo = 250
        self.maxEAmmo = 250
        self.regenCounter = 0
        self.regenMax = 10
        self.player = pygame.image.load('wiz.png').convert_alpha()
        self.player = pygame.transform.scale(self.player, (width, height))
        self.player = pygame.transform.flip(self.player, 1 ,0)
        self.tempPlayer = self.player
        self.maxhp = 500
        self.o1, self.o2, self.o3, self.o4, self.o5 = None, None, None, None, None
        self.qSheet = SpriteSheet("wizQsheet.png", 4, 3, 9, None, None, 2)
        self.qFrame = 0
        self.qX, self.qY = 0,0
        self.isQ = False
        self.qHitBox = pygame.Rect(self.qSheet.cells[0])
        self.qDmg = 70
        self.isTp = False
        self.tpSheet = SpriteSheet("tp.png", 8, 8, 64, width, height, 1.8)
        self.tpFrame = 0
        self.tempX, self.tempY = 0,0
        self.shoot = 0
        self.shootRate = 11

    def draw1(self, win):
        for bullet in self.bullets:
            bullet.draw(win)
        if self.isQ:
            self.qSheet.draw(win, self.qFrame//4, self.qX, self.qY, 1)
        if self.isTp:
            self.tpSheet.draw(win, 64 - self.tpFrame, self.x + self.width//2, self.y + self.height//4, 1)
            self.tpSheet.draw(win, self.tpFrame, self.tempX, self.tempY, 1)

    def update1(self, mouseX, mouseY, boardX, boardY):
        self.regenCounter += 1
        if self.regenCounter % self.regenMax == 0:
            self.hp += 1
        if self.qAmmo < self.maxQAmmo:
            self.qAmmo += 1
        if self.eAmmo < self.maxEAmmo:
            self.eAmmo += 1
        if self.isUlt == True:
            self.frostOrbs()
        elif self.ultAmmo >= self.maxUltAmmo:
            self.ultAmmo = self.maxUltAmmo
        for bullet in self.bullets:
            if not isinstance(bullet, FrostOrb):
                if bullet.x > boardX + 2*bullet.width  or bullet.x < -2 * bullet.width:
                    self.bullets.remove(bullet)
                elif bullet.y > boardY + 2*bullet.height  or bullet.y < -2 * bullet.height:
                    self.bullets.remove(bullet)
        if self.isQ:
            self.qFrame += 1
            if self.qFrame >= 36:
                self.isQ = False
        if self.isTp:
            self.tpFrame += 1
            if self.tpFrame >= 64:
                self.isTp = False
        for bullet in self.bullets:
            bullet.update()
        if self.isShoot and self.shoot % self.shootRate == 0:
            self.clickSkill(mouseX, mouseY)
        self.shoot += 1
    
    def clickSkill(self, mouseX, mouseY):
        y = self.y + self.height/2
        if self.left == True:
            x = self.x - self.width / 7
        else:
            x = self.x + self.width - self.width/7
        vec = Functions.unitVector((x, y), (mouseX, mouseY))
        angle = Functions.getRotation(0, *vec)
        self.bullets.append(self.wizBullet(x, y, *vec, angle))

    def wizBullet(self, x, y, vX, vY, angle):
        return WizBullet(x, y, 30, 30, vX, vY, 7, angle)
    
    def startUlt(self):
        if self.ultAmmo == self.maxUltAmmo:
            self.isUlt = True
            orbs = 5
            s = 360 / orbs
            w, h = 200, 200
            self.o1 = FrostOrb(self.x, self.y, 1*s, w, h)
            self.o2 = FrostOrb(self.x, self.y, 2*s, w, h)
            self.o3 = FrostOrb(self.x, self.y, 3*s, w, h)
            self.o4 = FrostOrb(self.x, self.y, 4*s, w, h)
            self.o5 = FrostOrb(self.x, self.y, 5*s, w, h)
            for orb in [self.o1,self.o2,self.o3,self.o4,self.o5]:
                self.bullets.append(orb)

    def frostOrbs(self):
        self.ultAmmo -= 0.5
        if self.ultAmmo <= 0:
            for orb in [self.o1,self.o2,self.o3,self.o4,self.o5]:
                if orb in self.bullets:
                    self.bullets.remove(orb)
            self.isUlt = False
            self.ultAmmo = 0

    def qSkill(self, mouseX, mouseY):
        if self.qAmmo == self.maxQAmmo:
            self.qHitBox.center = (mouseX, mouseY)
            self.qAmmo = 0
            self.qX, self.qY = mouseX, mouseY
            self.isQ = True
            self.qFrame = 0

    def eSkill(self, mouseX, mouseY, rocks):
        if self.eAmmo == self.maxEAmmo:
            tp = True
            bX, bY = self.x, self.y
            self.x, self.y = mouseX - self.width//2, mouseY - self.height//2
            self.hitbox = pygame.Rect(self.x,self.y,self.width,self.height)
            for rock in rocks:
                if rock.hitbox.colliderect(self.hitbox):
                    tp = False
                    self.x, self.y = bX, bY
                    break
            if tp:
                self.isTp = True
                self.tpFrame = 0
                self.eAmmo = 0
                self.tempX, self.tempY = self.x + self.width//2, self.y + self.y //2
                self.x, self.y = mouseX - self.width//2, mouseY - self.height//2
        