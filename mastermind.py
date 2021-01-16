import pygame
from pygame.locals import *
import random
import numpy

pygame.init()
pygame.display.set_icon(pygame.image.load("Assets/Branding/window_icon.png"))
pygame.display.set_caption("Mastermind by KL Corporation")
window_size = (600, 900)
window = pygame.display.set_mode(window_size)

mastermind_array = []
gameboard = numpy.zeros((12, 4), dtype="int8")

current_row = 0

rects = []
for y in range(len(gameboard)):
    row = []
    for x in range(len(gameboard[0])):
        row.append(pygame.Rect(x*90+150,y*70+50, 60, 60))
    rects.append(row)

selection_rects = []

for y in range(6):
    selection_rects.append(pygame.Rect(510, 400 + y*50, 40, 40))

def isfull(row: list) -> bool:
    for x in row:
        if not x:
            return False
    return True

class Colors:
    Red = (255, 0, 0)
    Yellow = (255, 255, 0)
    Green = (0, 255, 0)
    Cyan = (0, 255, 255)
    Blue = (0, 0, 255)
    Magenta = (255, 0, 255)
    White = (255, 255, 255)
    LightGray = (192, 192, 192)
    Gray = (128, 128, 128)
    DarkGray = (64, 64, 64)
    Black = (0, 0, 0)


gamecolors = {
    0: Colors.White,
    1: Colors.Yellow,
    2: Colors.Green,
    3: Colors.Cyan,
    4: Colors.Blue,
    5: Colors.Magenta,
    6: Colors.Gray
}

color_amounts = dict()
while len(mastermind_array) < 4:
    f = random.randint(1, len(gamecolors)-1)
    mastermind_array.append(f)
    try: color_amounts[f] += 1
    except KeyError: color_amounts[f] = 1
print(color_amounts)

def checkIfCorrect(ver1, ver2):
    for x, x1 in zip(ver1, ver2):
        if x != x1:
            return False
    return True

def checkHowManyColorsAreCorrect(cArray, tArray):
    ct = 0
    color_amounts_C = color_amounts.copy()
    for unit in tArray:
        if unit in color_amounts_C.keys():
            if color_amounts_C[unit]:
                ct += 1
                color_amounts_C[unit] -= 1
    del color_amounts_C
    return ct

def checkHowManyColorsAreInRightPlace(cArray, tArray):
    ct = 0
    for c, t in zip(cArray, tArray):
        if c == t: ct += 1
    return ct

def win():
    window.blit(pygame.font.SysFont("Arial", 40).render("Voitit pelin!", False, (255, 20, 65)), (5, 100))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

def lose():
    window.blit(pygame.font.SysFont("Arial", 40).render("Havisit pelin!", False, (255, 20, 65)), (5, 100))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

class Indicator:
    def __init__(self, c1, c2, p):
        self.pos = p
        print("c1", c1, "c2", c2)
        self.s = pygame.Surface((100, 35))
        self.s.fill((128, 129, 128))
        for r in range(c1):
            pygame.draw.rect(self.s, (255, 0, 0), (r*22, 1, 12, 12))
        for r in range(c2):
            pygame.draw.rect(self.s, (0, 255, 0), (r*22, 18, 12, 12))
        #self.s.set_colorkey((255, 255, 255))
    def render(self, surf: pygame.Surface):
        surf.blit(self.s, self.pos)

placement_color_index = 1

print(mastermind_array)

indicators = list()

main_running = True
while main_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                placement_color_index -= 1
                if placement_color_index < 1:
                    placement_color_index = len(gamecolors) - 1
            elif event.button == 5:
                placement_color_index += 1
                if placement_color_index > len(gamecolors) - 1:
                    placement_color_index = 1

    window.fill((110, 40, 19))
    if current_row < 12 and isfull(gameboard[11 - current_row]):
        """checkHowManyColorsAreCorrect(mastermind_array, gameboard[-current_row - 1])"""
        indicators.append(Indicator(checkHowManyColorsAreCorrect(mastermind_array, gameboard[-current_row - 1]), checkHowManyColorsAreInRightPlace(mastermind_array, gameboard[-current_row - 1]), (20, (11 - current_row) * 70 + 70)))
        current_row += 1
        
    for indicator in indicators: indicator.render(window)
    
    for y in range(len(gameboard)):
        for x in range(len(gameboard[0])):
            pygame.draw.circle(window, gamecolors[gameboard[y][x]], (x*90 + 180, y*70 + 80), 28)
            highlight = False
            if rects[y][x].collidepoint(pygame.mouse.get_pos()):
                highlight = True
                col = Colors.Red
                if (11 - y) == current_row and pygame.mouse.get_pressed()[0]:
                        gameboard[y][x] = placement_color_index
            else:
                col = Colors.Black
            if highlight:
                tsurf = pygame.Surface((60, 60))
                pygame.draw.circle(tsurf, gamecolors[placement_color_index], (30, 30), 30)
                tsurf.set_colorkey((0, 0, 0))
                tsurf.set_alpha(96.69)
                window.blit(tsurf, (x*90 + 150, y*70 + 50))
            pygame.draw.circle(window, col, (x*90 + 180, y*70 + 80), 30, 2)
    if current_row < 12:
        pygame.draw.rect(window, (0, 0, 0), (120, 815 - current_row * 70, 380, 70), 4)
    
    if checkIfCorrect(mastermind_array, gameboard[11-current_row]):
        _break = win()
        if _break: main_running = False

    if current_row > 11:
        _break = lose()
        if _break: main_running = False
        
    yuewae = 0
    for unit in selection_rects:
        if yuewae == placement_color_index - 1:
            pygame.draw.rect(window, (0, 0, 0), (unit.x - 2, unit.y - 2, unit.width + 2, unit.height + 2), 4)
        if unit.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, (0, 0, 0), unit, 10)
            if pygame.mouse.get_pressed()[0]:
                placement_color_index = yuewae + 1
        pygame.draw.rect(window, gamecolors[yuewae + 1], unit)
        yuewae += 1
    
    
    
    pygame.display.update()

pygame.quit()