######################匯入模組######################

import pygame
import sys

######################初始化######################

pygame.init()  # 啟動pygame
width = 640  # 設定視窗寬度
height = 320  # 設定視窗高度
######################建立視窗及物件######################

# 設定視窗大小
screen = pygame.display.set_mode((width, height))  # 建立視窗
# 設定視窗標題
pygame.display.set_caption("my game")  # 設定視窗標題
######################建立畫布######################

# 建立畫布
bg = pygame.Surface((width, height))  # 建立畫布
# 畫布為白色
bg.fill((255, 255, 255))  # 畫布為白色
######################繪製圖形######################

# 畫圓形(畫布, 顏色, 圓心座標, 半徑)
pygame.draw.circle(bg, (0, 0, 255), (200, 100), 30, 0)  # 畫圓形
pygame.draw.circle(bg, (0, 0, 255), (400, 100), 30, 0)  # 畫圓形
# 畫矩形(畫布, 顏色, 矩形座標, 寬度, 高度)
pygame.draw.rect(bg, (0, 255, 0), (270, 130, 60, 40), 5)  # 畫矩形
# 畫橢圓(畫布, 顏色, [x, y, 寬, 高], 線寬)
pygame.draw.ellipse(bg, (255, 0, 0), [130, 160, 60, 35], 5)  # 畫橢圓
pygame.draw.ellipse(bg, (255, 0, 0), [400, 160, 60, 35], 5)  # 畫橢圓
# 畫線, (畫布, 顏色, 起點座標, 終點座標, 線寬)
pygame.draw.line(bg, (255, 0, 255), (280, 220), (320, 220), 3)  # 畫線
######################循環偵測######################

while True:  # 無限迴圈
    for event in pygame.event.get():  # 取得事件
        if event.type == pygame.QUIT:  # 如果事件是關閉視窗 (X)
            sys.exit()  # 結束程式

    # 取得滑鼠按鍵狀態
    buttons = pygame.mouse.get_pressed()
    if buttons[0]:  # 如果左鍵被按下
        # 取得滑鼠位置
        x, y = pygame.mouse.get_pos()
        # 在滑鼠位置畫圓
        pygame.draw.circle(bg, (0, 0, 0), (x, y), 10, 0)

    # 更新畫面
    screen.blit(bg, (0, 0))
    pygame.display.update()  # 更新畫面
