#Luke Scatchard
#5/20/20
#kamaitachi game (i havent decided what to call it yet)

import pygame, sys, math, random
from pygame.locals import *
from pygame import gfxdraw
from PIL import Image

pygame.init()
fpsClock=pygame.time.Clock()

screen = pygame.display.set_mode((928,534))
pygame.display.set_caption('jebrjf')
myfont = pygame.font.SysFont("monospace", 20)

bg_layer_1 = pygame.image.load('bg_2x.png')
bg_layer_1_x = 0
bg_layer_2 = pygame.image.load('bg2.png')
bg_layer_2_x = 0
bg_layer_2_x2 = (bg_layer_2.get_width())

left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False

spawn_counter = 0
sawn_rand = 0


def OnGround(player):

    blocks_hit_list = pygame.sprite.pygame.sprite.spritecollide(player, blocklist, False)
    
    if len(blocks_hit_list) >= 1:
        for block in blocks_hit_list:
            if player.y+50 <= block.y and player.y+64 >= block.y:
                player.y = block.y-64
                return True
            elif player.y+50 > block.y and player.y <= block.y+26 and player.x > block.leftx+16:
                if player.speed <= 0:
                    player.speed = 0
            elif player.y+50 > block.y and player.y <= block.y+26 and player.x < block.leftx+16:
                if player.speed >= 0:
                    player.speed = 0
            elif player.y >= block.y+26:
                player.jumppower = -2
            return False
    else:
        return False

def CollectCoins(player):
    coinlist = pygame.sprite.pygame.sprite.spritecollide(player, coins, True)

def DrawWindow():
    screen.blit(bg_layer_1, (bg_layer_1_x, 0))
    screen.blit(bg_layer_2, (bg_layer_2_x, 213))
    screen.blit(bg_layer_2, (bg_layer_2_x2, 213))
    screen.blit(MAIN_PLAYER.image, (MAIN_PLAYER.x, MAIN_PLAYER.y))
    for i in blocklist:
        screen.blit(i.image, (i.leftx, i.y))
    for i in coins:
        #if i.collected == False:
        screen.blit(i.image, (i.xleft, i.ytop))
    for i in enemylist:
        screen.blit(i.image, (i.x, i.y))
    pygame.display.update()

class Player(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        
        self.x = 120
        self.y = 13*32
        self.speed = 0
        self.jumpcounter = 0
        self.jumppower = 8
        self.jumping = False
        self.whichimage = 1
        self.state = "air"
        self.image = pygame.image.load('kamaitachi.png')
        self.rect = pygame.Rect(self.x, self.y, 64, 64)

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

        self.state = "air"

        if OnGround(MAIN_PLAYER): 
            self.state = "ground"
            self.jumppower = 8

        if self.state != "ground":
            self.y -= self.jumppower
            self.jumpcounter += 1
            #decreases jump power every six frames
            #raise to make jump floatier and lower to make more tight
            if self.jumpcounter > 4:
                self.jumppower -= 1
                self.jumpcounter = 0

        self.x += self.speed

        if self.x > 866:
            self.x = 866
        elif self.x < 0:
            self.x = 0

        self.rect = pygame.Rect(self.x, self.y, 64, 64)


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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):

        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load('thundermuffin.png')
        self.image2 = pygame.image.load('thundermuffin2.png')
        self.image3 = pygame.image.load('thundermuffin3.png')
        self.image = self.image3
        self.speed = speed
        self.state = "ground"
        self.jumppower = 5
        self.jumpcounter = 4
        self.x = xpos
        self.y = ypos
        self.rect = pygame.Rect(xpos+3, ypos+19, 58, 42)
        self.imageswitch = 0
    
    def switchimage(self):
        self.imageswitch += 1
        if self.imageswitch <= 19:
            self.image = self.image1
        else:
            self.image = self.image2

        if self.imageswitch == 39:
            self.imageswitch = 0

    def move(self):

        self.state = "air"

        if OnGround(self): 
            self.state = "ground"
            self.jumppower = 5

        if self.state != "ground":
            self.y -= self.jumppower
            self.jumpcounter += 1
            #decreases jump power every six frames
            #raise to make jump floatier and lower to make more tight
            if self.jumpcounter > 4:
                    self.jumppower -= 1
                    self.jumpcounter = 0

        self.x += self.speed

        if self.x > 866 or self.x < 0:
            self.speed *= -1

        self.rect = pygame.Rect(self.x+3, self.y+19, 58, 42)

class Blocks(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, sprite):

        pygame.sprite.Sprite.__init__(self)

        if sprite == 1:
            self.image = pygame.image.load('block.png')
            self.rect = pygame.Rect(xpos, ypos, 32, 32)
        elif sprite == 2:
            self.image = pygame.image.load('blocklooong.png')
            self.rect = pygame.Rect(xpos, ypos, 1820, 64)
        
        self.leftx = xpos
        self.rightx = xpos + self.image.get_width()
        self.y = ypos
        self.blocks_speed = 1.2

class Coin(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos):

        pygame.sprite.Sprite.__init__(self)

        self.xleft = xpos
        self.xright = xpos+64
        self.ytop = ypos
        self.ybtm = ypos+64
        self.image = self.image = pygame.image.load('kkoin.png')
        self.rect = pygame.Rect(xpos, ypos, 64, 64)
        self.collected = False
    
#adding coins to stage
coins = pygame.sprite.Group()
coins.add(Coin(32, 8*32))
coins.add(Coin(26*32, 8*32))   

#adding blocks to stage
blocklist = pygame.sprite.Group()
blocklist.add(Blocks(0, 15*32, 2))

#middle left
blocklist.add(Blocks(0, 10*32, 1))
blocklist.add(Blocks(32, 10*32, 1))
blocklist.add(Blocks(2*32, 10*32, 1))
blocklist.add(Blocks(3*32, 10*32, 1))

#middle right
blocklist.add(Blocks(28*32, 10*32, 1))
blocklist.add(Blocks(27*32, 10*32, 1))
blocklist.add(Blocks(26*32, 10*32, 1))
blocklist.add(Blocks(25*32, 10*32, 1))

#middle center
blocklist.add(Blocks(12*32, 10*32, 1))
blocklist.add(Blocks(13*32, 10*32, 1))
blocklist.add(Blocks(14*32, 10*32, 1))
blocklist.add(Blocks(15*32, 10*32, 1))
blocklist.add(Blocks(16*32, 10*32, 1))
blocklist.add(Blocks(17*32, 10*32, 1))

#top left
blocklist.add(Blocks(6*32, 5*32, 1))
blocklist.add(Blocks(7*32, 5*32, 1))
blocklist.add(Blocks(8*32, 5*32, 1))
blocklist.add(Blocks(9*32, 5*32, 1))

#top right
blocklist.add(Blocks(20*32, 5*32, 1))
blocklist.add(Blocks(21*32, 5*32, 1))
blocklist.add(Blocks(22*32, 5*32, 1))
blocklist.add(Blocks(23*32, 5*32, 1))

enemylist = pygame.sprite.Group()
# spawn_rand = random.randint(1, 2)
# if spawn_rand == 1:
#     enemylist.add(Enemy(8*32, 3*32, -3))
# elif spawn_rand == 2:
#     enemylist.add(Enemy(21*32, 3*32, -3))
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
    for i in enemylist:
        i.switchimage()
        i.move()
    
    spawn_counter += 1
    if spawn_counter >= 300:
        spawn_rand = random.randint(1, 200)
        if spawn_rand == 1:
            enemylist.add(Enemy(8*32, 3*32, 3))
            spawn_counter = 100
        elif spawn_rand == 2:
            enemylist.add(Enemy(21*32, 3*32, -3))
            spawn_counter = 100


    DrawWindow()

    pygame.display.update()
    fpsClock.tick(60)

