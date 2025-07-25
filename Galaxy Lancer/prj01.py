###################### 載入套件 ######################
import pygame
import sys
import os

# 設定工作目錄為目前檔案所在路徑，確保圖片路徑正確
os.chdir(sys.path[0])

###################### 初始化設定 ######################
pygame.init()  # 啟動pygame

###################### 遊戲視窗設定 ######################
win_width = 480  # 視窗寬度
win_height = 640  # 視窗高度
win_size = (win_width, win_height)
screen = pygame.display.set_mode(win_size)  # 建立視窗
pygame.display.set_caption("Galaxy Lancer - Space Scrolling")  # 設定視窗標題

###################### 主程式迴圈 ######################
clock = pygame.time.Clock()

###################### 載入背景圖片 ######################
try:
    bg_path = os.path.join("image", "space.png")
    if os.path.exists(bg_path):
        bg_image = pygame.image.load(bg_path).convert()
        print(f"[載入成功] {bg_path}")
        # 取得圖片原始尺寸，並將視窗設為3/4
        img_width = bg_image.get_width()
        img_height = bg_image.get_height()
        win_width = int(img_width * 0.75)
        win_height = int(img_height * 0.75)
        win_size = (win_width, win_height)
        # 取得螢幕解析度，計算置中座標
        info = pygame.display.Info()
        screen_x = (info.current_w - win_width) // 2
        screen_y = (info.current_h - win_height) // 2
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{screen_x},{screen_y}"
        screen = pygame.display.set_mode(win_size)
    else:
        bg_image = None
        print(f"[找不到圖片] {bg_path}")
except Exception as e:
    bg_image = None
    print(f"[背景圖片載入失敗] {e}")

# 背景捲動參數
bg_y = 0  # 背景圖片的初始y座標
bg_speed = 2  # 捲動速度（每幀向下移動2像素）

while True:
    clock.tick(200)  # 設定FPS為200
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # ======================== 背景捲動繪製 ========================
    # 若成功載入背景圖片，則進行捲動繪製
    if bg_image:
        # 1. 先繪製第一張背景，座標為 (0, bg_y)
        # 2. 再繪製第二張背景，座標為 (0, bg_y - 背景高度)，讓兩張圖片上下銜接
        # 3. 每次迴圈讓bg_y增加，背景向下捲動
        # 4. 當第一張背景完全移出視窗時，重設bg_y為0，實現無縫循環
        screen.blit(bg_image, (0, bg_y))
        screen.blit(bg_image, (0, bg_y - bg_image.get_height()))
        bg_y += bg_speed
        if bg_y >= bg_image.get_height():
            bg_y = 0
    else:
        # 若背景圖片載入失敗，則以黑色填滿視窗
        screen.fill((0, 0, 0))
    # ===========================================================
    pygame.display.update()  # 更新畫面
