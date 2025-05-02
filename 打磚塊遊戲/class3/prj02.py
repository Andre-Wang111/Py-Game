######################載入套件######################
import pygame
import sys
import random

######################物件類別######################
pygame.init()


class Brick:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hit = False

    def draw(self, display_area):
        if not self.hit:
            pygame.draw.rect(display_area, self.color, self.rect)


######################定義函式區######################

######################初始化設定######################

######################載入圖片######################

######################遊戲視窗設定######################
bg_x = 800
bg_y = 600
bg_size = (bg_x, bg_y)
pygame.display.set_caption("打磚塊遊戲")
screen = pygame.display.set_mode(bg_size)
######################磚塊######################
bricks_row = 9
bricks_col = 11
brick_w = 58
brick_h = 16
brick_gap = 2
bricks = []
for col in range(bricks_col):
    for row in range(bricks_row):
        x = col * (brick_w + brick_gap) + 70
        y = row * (brick_h + brick_gap) + 60
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        brick = Brick(x, y, brick_w, brick_h, color)
        bricks.append(brick)
######################顯示文字設定######################

######################底板設定######################

######################球設定######################

######################遊戲結束設定######################

######################主程式######################
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for brick in bricks:
        brick.draw(screen)
    pygame.display.update()
