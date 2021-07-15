import math
import random
class Functions(object):
    def __init__():
        pass
    @staticmethod
    def unitVector(start, end):
        (sX, sY) = start
        (eX, eY) = end
        dx = eX - sX
        dy = eY - sY
        mag = math.sqrt(dx**2 + dy**2)
        return (dx/mag, dy/mag)

    @staticmethod
    def getDist(a,b):
        return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
        
    @staticmethod
    def getRotation(angleFrom0, vX, vY):
        # Zero goes in positive X -------->
        # angleFrom0 is in degrees
        if vX == 0:
            if vY >= 0:
                vecAngle = 90
            else:
                vecAngle = -90
        else:
            vecAngle = math.atan(vY/vX) * (180 / math.pi)
        if vX < 0:
            vecAngle += 180
        return angleFrom0 - vecAngle

    @staticmethod
    def randomPos(boardX, boardY, rectX, rectY):
        # for around edge of board
        # 1 is top, the rotate clockwise
        bound = max(rectX, rectY)
        edgeNumb = random.randint(1,4)
        if edgeNumb == 1:
            mag = random.randint(-bound, boardX)
            return (mag, -rectY)
        if edgeNumb == 2:
            mag = random.randint(-bound, boardY)
            return (boardX, mag)
        if edgeNumb == 3:
            mag = random.randint(-bound, boardX)
            return (mag, boardY)
        if edgeNumb == 4:
            mag = random.randint(-bound, boardY)
            return(-rectX, mag)
    
    def cooldownTemplate(self):
        #Copy paste
        ammoPerc = self.p1.ultAmmo / self.p1.maxUltAmmo
        if ammoPerc == 1:
            color = (204, 204, 0)
        else:
            blue = 180 - 150 * ammoPerc
            color = (255,255, blue)
        pygame.draw.rect(win, color, (self.w//10, self.h//20, 4*ammoPerc*self.w//5, self.h//20))
        pygame.draw.rect(win, (204,204,0), (self.w//10, self.h//20, 4*self.w//5, self.h//20), width = 3)
        if ammoPerc == 1:
            f = pygame.font.Font(None, 30)
            t = f.render("PRESS R TO USE SPECIAL", True, (70,70,0))
            tRect = t.get_rect()
            tRect.center = (self.w//2, 3*self.h//40)
            win.blit(t, tRect)
    @staticmethod    
    def randomPos2(boardX, boardY, rectX, rectY):
        minX, minY = rectX, rectY
        maxX, maxY = boardX - rectX, boardY - rectY
        x = random.randint(minX, maxX)
        y = random.randint(minY, maxY)
        return (x,y)

    @staticmethod
    def closestIn(target, List):
        minDist, minEle = None, None
        for item in List:
            dist = Functions.getDist(target, item)
            if minDist == None or dist < minDist:
                minDist = dist
                minEle = item
        return minEle
    
    def rotary(ox, oy, nx, ny, nWeight):
        # nWeight is how much turning weight has
        nx, ny = Functions.unitVector((0,0), (nx, ny))
        vx = ox + nx * nWeight
        vy = oy + ny * nWeight
        vec = Functions.unitVector((0,0), (vx, vy))
        return vec



