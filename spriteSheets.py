import pygame

# Adapted version of code.Pylet https://www.youtube.com/watch?v=mfX3XQv9lnI

class SpriteSheet(object):
    def __init__(self, filename, cols, rows, cellN, width, height, scale = 1):
        self.sheet = pygame.image.load(filename).convert_alpha()
        if width != None:
            self.sheet = pygame.transform.scale(self.sheet, (width * cols, height * rows))
        self.sheet = pygame.transform.rotozoom(self.sheet, 0, scale)
        self.cols = cols
        self.rows = rows
        self.cellN = cellN
        self.rect = self.sheet.get_rect()
        self.cellW = self.rect.width / cols
        self.cellH = self.rect.height / rows
        self.cells = [(i % cols * self.cellW, i // cols * self.cellH, self.cellW, self.cellH) for i in range(cellN)]
    def draw(self, win, index, x, y, mode):
        modes = [(0,0), (- self.cellW//2, - self.cellH//2)]
        oX, oY = modes[mode]
        win.blit(self.sheet, (x + oX,y + oY), self.cells[index])