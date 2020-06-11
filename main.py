#Luke Scatchard
#5/20/20
#kamaitachi game (i havent decided what to call it yet)

import pygame, sys, math, random
from pygame.locals import *
from pygame import gfxdraw
from PIL import Image
#from player import *

pygame.init()
fpsClock=pygame.time.Clock()

screen = pygame.display.set_mode((928,534))
pygame.display.set_caption('jebrjf')

bg_layer_1 = pygame.image.load('bg_2x.png')
bg_layer_1_x = 0
bg_layer_2 = pygame.image.load('bg2.png')
bg_layer_2_x = 0
bg_layer_2_x2 = (bg_layer_2.get_width())

left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False

coins_collected = 0
coin_removal = 0

#this collision engine is brought to you by ray peng
def OnGround(player):

    for blocks in blocklist:
        if blocks.leftx < player.x + 64 or blocks.rightx > player.x:
            if blocks.y + 32 == player.y:
                player.jumppower = 0
                return False
        if blocks.leftx < player.x + 64 or blocks.rightx > player.x:
            if blocks.y == player.y + 64:
                return True
            else:
                return False

def CollectCoins(player):
    global coins_collected

    for i in coins:
        if (i.xright > player.x) or (player.x+64 < i.xleft):
            if (i.ytop < player.y) or (i.ybtm > player.y+64):
                coins_collected += 1
                i.collected = True

def DrawWindow():
    screen.blit(bg_layer_1, (bg_layer_1_x, 0))
    screen.blit(bg_layer_1, (bg_layer_1_x2, 0))
    screen.blit(bg_layer_2, (bg_layer_2_x, 213))
    screen.blit(bg_layer_2, (bg_layer_2_x2, 213))
    screen.blit(MAIN_PLAYER.image, (MAIN_PLAYER.x, MAIN_PLAYER.y))
    for i in blocklist:
        screen.blit(i.image, (i.leftx, i.y))
    for i in coins:
        #if i.collected == False:
        screen.blit(i.image, (i.xleft, i.ytop))
    pygame.display.update()

class Player:
    def __init__(self):
        self.x = 120
        self.y = 13*32
        self.speed = 0
        self.jumpcounter = 0
        self.jumppower = 7
        self.jumping = False
        self.whichimage = 1
        self.image = pygame.image.load('kamaitachi.png')

    def move(self):

        if left_pressed == True:
            if self.speed >= -3.0:
                 self.speed -= 1.0
            else:
                self.speed = -3.0
        elif right_pressed == True:
            if self.speed <= 3.0:
                self.speed += 1.0
            else:
                self.speed = 3.0
        else:
            self.speed = 0

        if (self.jumping == True):
            self.y -= self.jumppower
            self.jumpcounter += 1
            #decreases jump power every six frames
            #raise to make jump floatier and lower to make more tight
            if down_pressed == False:
                if self.jumpcounter > 5:
                    self.jumppower -= 1
                    self.jumpcounter = 0
            #stops jumping once on the ground
            if OnGround(MAIN_PLAYER) == True:
                self.jumping = False
                self.jumppower = 7

        self.x += self.speed

        if self.x > 866:
            self.x = 866
        elif self.x < 0:
            self.x = 0


    def update(self):
        if right_pressed == True:
            if self.whichimage <= 9:
                self.image = pygame.image.load('kamaitachi.png')
            else:
                self.image = pygame.image.load('kamaitachi2.png')
        elif left_pressed == True:
            if self.whichimage <= 9:
                self.image = pygame.image.load('kamaitachileft.png')
            else:
                self.image = pygame.image.load('kamaitachileft2.png')

        if OnGround(MAIN_PLAYER) and self.speed != 0:
            self.whichimage += 1
            if self.whichimage == 19:
                self.whichimage = 0

class Blocks:
    def __init__(self, xpos, ypos, sprite):
        if sprite == 1:
            self.image = pygame.image.load('block.png')
        elif sprite == 2:
            self.image = pygame.image.load('blocklooong.png')
        self.leftx = xpos
        self.rightx = xpos + self.image.get_width()
        self.y = ypos
        self.blocks_speed = 1.2

class Coin:
    def __init__(self, xpos, ypos):
        self.xleft = xpos
        self.xright = xpos+64
        self.ytop = ypos
        self.ybtm = ypos+64
        self.image = self.image = pygame.image.load('kkoin.png')
        self.collected = False
    
coins = []
coins.append(Coin(32, 8*32))
coins.append(Coin(26*32, 8*32))   

blocklist = []
# for counter in range(30):
#     blocklist.append(Blocks(counter*32, 8*32, 1))
blocklist.append(Blocks(0, 15*32, 2))

blocklist.append(Blocks(0, 10*32, 1))
blocklist.append(Blocks(32, 10*32, 1))
blocklist.append(Blocks(2*32, 10*32, 1))
blocklist.append(Blocks(3*32, 10*32, 1))

blocklist.append(Blocks(28*32, 10*32, 1))
blocklist.append(Blocks(27*32, 10*32, 1))
blocklist.append(Blocks(26*32, 10*32, 1))
blocklist.append(Blocks(25*32, 10*32, 1))

blocklist.append(Blocks(12*32, 10*32, 1))
blocklist.append(Blocks(13*32, 10*32, 1))
blocklist.append(Blocks(14*32, 10*32, 1))
blocklist.append(Blocks(15*32, 10*32, 1))
blocklist.append(Blocks(16*32, 10*32, 1))
blocklist.append(Blocks(17*32, 10*32, 1))

MAIN_PLAYER = Player()

rungame = True
while rungame:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rungame = False
        elif event.type == KEYDOWN and event.key == pygame.K_a:
            left_pressed = True
            right_pressed = False
        elif event.type == KEYDOWN and event.key == pygame.K_d:
            right_pressed = True
            left_pressed = False
        elif event.type == KEYDOWN and event.key == pygame.K_w:
            if not (MAIN_PLAYER.jumping):
                MAIN_PLAYER.jumping = True
            up_pressed = True
        else:
            up_pressed = False
            left_pressed = False
            right_pressed = False
        
        if event.type == KEYDOWN and event.key == pygame.K_s:
            down_pressed = True
        else:
            down_pressed = False

    #screen.blit(track, (0,0))
    #MAIN_PLAYER.turn(Count)

    MAIN_PLAYER.move()
    MAIN_PLAYER.update()
    CollectCoins(MAIN_PLAYER)

    DrawWindow()

    pygame.display.update()
    fpsClock.tick(60)

