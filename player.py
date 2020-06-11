#Player class
import pygame, sys, math, random
from pygame.locals import *
from pygame import gfxdraw
from PIL import Image
from main import *

# class Player:
#     def __init__(self):
#         self.x = 120
#         self.y = 200
#         self.speed = 0
#         self.jumpspeed = 0
#         self.jumppower = 5
#         self.direction = 180 
#         self.image = pygame.image.load('kamaitachi.png')
    
#     def move(self):
        
#         if left_pressed == True:
#             if self.speed >= -5.0:
#                  self.speed -= 1.0
#             else:
#                 self.speed = -5.0
#         elif right_pressed == True:
#             if self.speed <= 5.0:
#                 self.speed += 1.0
#             else:
#                 self.speed = 5.0
#         else:
#             if self.speed > 0:
#                 self.speed -= 0.5
#             elif self.speed < 0:
#                 self.speed += 0.5

#         if up_pressed == True and OnGround(MAIN_PLAYER):
#             self.y += self.jumppower
#             self.jumppower -= 1.0
#         elif self.y >= OnGround(MAIN_PLAYER):
#             self.y += self.jumppower
#             self.jumppower -= 2.0
#         else:
#             self.jumppower = 0

        

#         self.x += self.speed
            

#     def update(self, right_pressed):
#         if right_pressed == True:
#             self.image = pygame.image.load('kamaitachi.png')
#         elif left_pressed == True:
#             self.image = pygame.image.load('kamaitachileft.png')