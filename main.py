# Luke Scatchard
# 5/20/20
# jebrjf

import pygame
import sys
import math
import random
from pygame.locals import *
from pygame import gfxdraw
from PIL import Image

pygame.init()
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((928, 534))
pygame.display.set_caption('jebrjf')
myfont = pygame.font.SysFont("monospace", 20)

bg_layer_1 = pygame.image.load('bg_2x.png')
bg_layer_1_x = 0
bg_layer_2 = pygame.image.load('bg2.png')
bg_layer_2_x = 0
bg_layer_2_x2 = (bg_layer_2.get_width())

left_pressed = False
right_pressed = False

bullet_counter = 0
enemies_killed = 0

spawn_counter = 0
sawn_rand = 0

#checks if a sprite is on the ground
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

#used to draw out all of the things
def DrawWindow():
    screen.blit(bg_layer_1, (bg_layer_1_x, 0))
    screen.blit(bg_layer_2, (bg_layer_2_x, 213))
    screen.blit(bg_layer_2, (bg_layer_2_x2, 213))
    screen.blit(MAIN_PLAYER.image, (MAIN_PLAYER.x, MAIN_PLAYER.y))
    for i in blocklist:
        screen.blit(i.image, (i.leftx, i.y))
    for i in enemylist:
        screen.blit(i.image, (i.x, i.y))
    for i in bulletlist:
        screen.blit(i.image, (i.x, i.y))
    pygame.display.update()

#player class controls the player
class Player(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.x = 150
        self.y = 13*32
        self.speed = 0
        self.jumpcounter = 0
        self.jumppower = 8
        self.jumping = False
        self.state = "air"
        self.image1 = pygame.image.load('kamaitachi.png')
        self.image2 = pygame.image.load('kamaitachileft.png')
        self.image = self.image1
        self.rect = pygame.Rect(self.x, self.y, 64, 64)

    def move(self):

        #moves the player
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

        #refills jumpyness when you touch the ground
        if OnGround(MAIN_PLAYER):
            self.state = "ground"
            self.jumppower = 8

        if self.state != "ground":
            self.y -= self.jumppower
            self.jumpcounter += 1
            # decreases jump power every six frames
            # raise to make jump floatier and lower to make more tight
            if self.jumpcounter > 4:
                self.jumppower -= 1
                self.jumpcounter = 0
        
        #moves player based on speed
        self.x += self.speed
        if self.x > 866:
            self.x = 866
        elif self.x < 0:
            self.x = 0

        #updates players collision
        self.rect = pygame.Rect(self.x, self.y, 64, 64)

    def update(self):
        #switches images based on direction player is facing
        if right_pressed == True:
            self.image = self.image1
        elif left_pressed == True:
            self.image = self.image2

#the bullet class controls the projectile things
class bullet(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        if MAIN_PLAYER.image == MAIN_PLAYER.image1:
            self.image = pygame.image.load('projectile.png')
            self.x = MAIN_PLAYER.x + 48
            self.speed = 5
        else:
            self.image = pygame.image.load('projectileleft.png')
            self.x = MAIN_PLAYER.x - 48
            self.speed = -5
        self.y = MAIN_PLAYER.y
        self.rect = pygame.Rect(self.x, self.y+5, 54, 42)

    def move(self):
        self.x += self.speed
        self.rect = pygame.Rect(self.x, self.y+5, 54, 42)

#the enemy class controls the thundermuffins
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
        #switches images a couple times per second
        #i just think it looks funny
        self.imageswitch += 1
        if self.imageswitch <= 19:
            self.image = self.image1
        else:
            self.image = self.image2

        if self.imageswitch == 39:
            self.imageswitch = 0

    def move(self):
        
        # movement is very similar to players except has smaller jumps 
        # and only switches direction when it hits a wall
        self.state = "air"

        if OnGround(self):
            self.state = "ground"
            self.jumppower = 5

        if self.state != "ground":
            self.y -= self.jumppower
            self.jumpcounter += 1
            # decreases jump power every six frames
            # raise to make jump floatier and lower to make more tight
            if self.jumpcounter > 4:
                    self.jumppower -= 1
                    self.jumpcounter = 0

        self.x += self.speed

        if self.x > 866 or self.x < 0:
            self.speed *= -1

        # updates thundermuffin collision
        self.rect = pygame.Rect(self.x+3, self.y+19, 58, 42)

    def collisioncheck(self, other):
        #checks if it is touching something and what it is touching
        #pretty much if the other thing has the same image as the player
        #then its the player and if its not its a bullet
        if pygame.sprite.collide_rect(self, other):
            if other.image == MAIN_PLAYER.image:
                return 'player death'
            else:
                return 'hit'

#the block class is used for all solid ground
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

# sets up and adds blocks to stage
    blocklist = pygame.sprite.Group()
    blocklist.add(Blocks(0, 15*32, 2))

    # middle left
    blocklist.add(Blocks(0, 10*32, 1))
    blocklist.add(Blocks(32, 10*32, 1))
    blocklist.add(Blocks(2*32, 10*32, 1))
    blocklist.add(Blocks(3*32, 10*32, 1))

    # middle right
    blocklist.add(Blocks(28*32, 10*32, 1))
    blocklist.add(Blocks(27*32, 10*32, 1))
    blocklist.add(Blocks(26*32, 10*32, 1))
    blocklist.add(Blocks(25*32, 10*32, 1))

    # middle center
    blocklist.add(Blocks(12*32, 10*32, 1))
    blocklist.add(Blocks(13*32, 10*32, 1))
    blocklist.add(Blocks(14*32, 10*32, 1))
    blocklist.add(Blocks(15*32, 10*32, 1))
    blocklist.add(Blocks(16*32, 10*32, 1))
    blocklist.add(Blocks(17*32, 10*32, 1))

    # top left
    blocklist.add(Blocks(6*32, 5*32, 1))
    blocklist.add(Blocks(7*32, 5*32, 1))
    blocklist.add(Blocks(8*32, 5*32, 1))
    blocklist.add(Blocks(9*32, 5*32, 1))

    # top right
    blocklist.add(Blocks(20*32, 5*32, 1))
    blocklist.add(Blocks(21*32, 5*32, 1))
    blocklist.add(Blocks(22*32, 5*32, 1))
    blocklist.add(Blocks(23*32, 5*32, 1))
# sets up enemy and bullet sprite groups
enemylist = pygame.sprite.Group()
bulletlist = pygame.sprite.Group()

MAIN_PLAYER = Player()

#main game loop
rungame = True
while rungame:
    #checks which keys youre pressing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rungame = False
        if event.type == KEYDOWN and event.key == pygame.K_a:
            left_pressed = True
            right_pressed = False
        elif event.type == KEYDOWN and event.key == pygame.K_d:
            right_pressed = True
            left_pressed = False
        else:
            left_pressed = False
            right_pressed = False

        #bullet counter is here to prevent players from spamming bullets
        if event.type == KEYDOWN and event.key == pygame.K_SPACE and bullet_counter >= 25:
            bullet_counter -= 25
            bulletlist.add(bullet())
    if bullet_counter < 100:
        bullet_counter += 1

    #moves the player
    MAIN_PLAYER.move()
    MAIN_PLAYER.update()
    #moves the bullet things
    for i in bulletlist:
        i.move()
    #moves the thundermuffins
    for i in enemylist:
        i.switchimage()
        i.move()
        if i.collisioncheck(MAIN_PLAYER) == 'player death':
            rungame = False
            print("can we get an f in the chat")
        for x in bulletlist:
            if i.collisioncheck(x) == 'hit':
                enemies_killed += 1
                print("You've killed " + str(enemies_killed) + " thundermuffins. Murderer.")
                enemylist.remove(i)

    #has enemies randomly spawn in
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

    

