######################匯入模組######################
import pygame
import sys

######################初始化######################
pygame.init()
width = 640
height = 320
######################建立視窗及物件######################
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")
######################循環偵測######################
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
