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
################建立畫布######################
# 建立畫布
bg = pygame.Surface((width, height))
# 畫布為白色
bg.fill((255, 255, 255))
#########################繪製圖形######################
# 繪製圓形
pygame.draw.circle(bg, (0, 0, 255), (200, 100), 30, 0)
pygame.draw.circle(bg, (0, 0, 255), (400, 100), 30, 0)
# 繪製矩形
pygame.draw.rect(bg, (0, 255, 0), (270, 130, 60, 40), 5)
# 繪製橢圓形
pygame.draw.ellipse(bg, (255, 0, 0), (130, 160, 60, 35), 5)
pygame.draw.ellipse(bg, (255, 0, 0), (400, 160, 60, 35), 5)
# 畫線
pygame.draw.line(bg, (255, 0, 255), (280, 220), (320, 220), 3)
# 繪製多邊形
pygame.draw.polygon(bg, (100, 200, 45), [[100, 100], [0, 200], [200, 200]], 0)
# 繪製圓弧
pygame.draw.arc(bg, (255, 10, 0), [100, 100, 100, 50], 0, 3.14, 5)
######################循環偵測######################
paint = False
color = (0, 255, 255)
while True:
    x, y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("click!!!")
            print(f"mouse pos: {x}, {y}")
            paint = not (paint)

    if paint:
        pygame.draw.circle(bg, color, (x, y), 10, 0)

    screen.blit(bg, (0, 0))  # 將畫布繪製於視窗左上角
    pygame.display.update()  # 更新視窗
