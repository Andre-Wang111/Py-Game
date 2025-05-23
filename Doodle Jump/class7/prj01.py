###################### 載入套件 ######################
import pygame
import sys


###################### Player 類別 ######################
class Player:
    def __init__(self, x, y, width, height, color):
        """
        初始化主角
        x, y: 主角左上角座標
        width, height: 主角寬高
        color: 主角顏色
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, display_area):
        """
        繪製主角
        display_area: 顯示畫布
        """
        pygame.draw.rect(display_area, self.color, self.rect)


###################### 初始化設定 ######################
pygame.init()  # 啟動pygame

###################### 遊戲視窗設定 ######################
win_width = 400
win_height = 600
win_size = (win_width, win_height)
screen = pygame.display.set_mode(win_size)  # 建立視窗
pygame.display.set_caption("Doodle Jump")  # 設定視窗標題

###################### 主角設定 ######################
player_width = 30
player_height = 30
player_color = (0, 255, 0)  # 綠色
player_x = win_width // 2 - player_width // 2  # 中間
player_y = win_height - 50 - player_height  # 底部上方50像素
player = Player(player_x, player_y, player_width, player_height, player_color)

###################### 主程式 ######################
clock = pygame.time.Clock()
while True:
    clock.tick(60)  # 設定FPS為60
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))  # 填滿黑色背景
    player.draw(screen)  # 繪製主角
    pygame.display.update()  # 更新畫面
