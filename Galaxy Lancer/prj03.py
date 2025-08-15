###################### 載入套件 ######################
import pygame  # 匯入pygame模組，負責遊戲視覺、音效等功能
import sys  # 匯入sys模組，提供系統相關功能（如取得執行路徑、結束程式）
import os  # 匯入os模組，負責檔案與目錄操作

# 設定工作目錄為目前檔案所在路徑，確保圖片路徑正確
os.chdir(
    sys.path[0]
)  # 將目前工作目錄切換到本程式檔案所在的資料夾，避免載入圖片時路徑錯誤

###################### 初始化設定 ######################
pygame.init()  # 初始化pygame，啟動所有pygame模組


###################### 遊戲視窗設定 ######################
win_width = 480  # 設定遊戲視窗的寬度為480像素
win_height = 640  # 設定遊戲視窗的高度為640像素
win_size = (win_width, win_height)  # 將寬度與高度組成一個tuple，作為視窗尺寸
screen = pygame.display.set_mode(win_size)  # 建立指定尺寸的遊戲視窗，並取得視窗物件
pygame.display.set_caption(
    "Galaxy Lancer - Space Scrolling"
)  # 設定視窗標題為"Galaxy Lancer - Space Scrolling"


###################### 主程式迴圈 ######################
clock = pygame.time.Clock()  # 建立一個Clock物件，用來控制遊戲迴圈的執行速度（FPS）


###################### 載入背景圖片 ######################
try:
    bg_path = os.path.join(
        "image", "space.png"
    )  # 組合背景圖片的路徑（image/space.png）
    if os.path.exists(bg_path):  # 檢查背景圖片檔案是否存在
        bg_image = pygame.image.load(
            bg_path
        ).convert()  # 載入背景圖片並轉換為適合顯示的格式
        print(f"[載入成功] {bg_path}")  # 印出載入成功訊息
        # 取得圖片原始尺寸，並將視窗設為3/4
        img_width = bg_image.get_width()  # 取得背景圖片的寬度
        img_height = bg_image.get_height()  # 取得背景圖片的高度
        win_width = int(img_width * 0.75)  # 將視窗寬度設為圖片寬度的3/4
        win_height = int(img_height * 0.75)  # 將視窗高度設為圖片高度的3/4
        win_size = (win_width, win_height)  # 更新視窗尺寸
        # 取得螢幕解析度，計算置中座標
        info = pygame.display.Info()  # 取得螢幕解析度資訊
        screen_x = (info.current_w - win_width) // 2  # 計算視窗置中時的x座標
        screen_y = (info.current_h - win_height) // 2  # 計算視窗置中時的y座標
        os.environ["SDL_VIDEO_WINDOW_POS"] = (
            f"{screen_x},{screen_y}"  # 設定視窗啟動時的位置（置中）
        )
        screen = pygame.display.set_mode(win_size)  # 重新建立新尺寸的視窗
    else:
        bg_image = None  # 若找不到圖片，設為None
        print(f"[找不到圖片] {bg_path}")  # 印出找不到圖片的訊息
except Exception as e:
    bg_image = None  # 若載入過程發生例外，設為None
    print(f"[背景圖片載入失敗] {e}")  # 印出錯誤訊息

# 背景捲動參數
bg_y = 0  # 設定背景圖片的初始y座標為0（從最上方開始）
bg_speed = 2  # 設定背景捲動速度，每幀向下移動2像素


###################### 載入主角圖片與初始位置 ######################
# 載入主角圖片（fighter_M.png），並設定初始位置於視窗正中央
try:
    # 預先載入三種主角圖片：中、左、右
    fighter_path_M = os.path.join("image", "fighter_M.png")  # 中立狀態圖片
    fighter_path_L = os.path.join("image", "fighter_L.png")  # 左移狀態圖片
    fighter_path_R = os.path.join("image", "fighter_R.png")  # 右移狀態圖片

    # 預設主角圖片為None
    fighter_img_M = fighter_img_L = fighter_img_R = None

    # 載入中立圖片
    if os.path.exists(fighter_path_M):
        fighter_img_M = pygame.image.load(fighter_path_M).convert_alpha()
        print(f"[載入成功] {fighter_path_M}")
    else:
        print(f"[找不到圖片] {fighter_path_M}")

    # 載入左移圖片
    if os.path.exists(fighter_path_L):
        fighter_img_L = pygame.image.load(fighter_path_L).convert_alpha()
        print(f"[載入成功] {fighter_path_L}")
    else:
        print(f"[找不到圖片] {fighter_path_L}")

    # 載入右移圖片
    if os.path.exists(fighter_path_R):
        fighter_img_R = pygame.image.load(fighter_path_R).convert_alpha()
        print(f"[載入成功] {fighter_path_R}")
    else:
        print(f"[找不到圖片] {fighter_path_R}")

    # 預設主角圖片為中立狀態
    fighter_img = fighter_img_M

    # 取得主角圖片尺寸（以中立圖為主）
    if fighter_img_M:
        fighter_w = fighter_img_M.get_width()
        fighter_h = fighter_img_M.get_height()
        # 設定主角初始座標為視窗正中央
        fighter_x = (win_width - fighter_w) // 2
        fighter_y = (win_height - fighter_h) // 2
    else:
        fighter_w = fighter_h = 0
        fighter_x = fighter_y = 0
        print("[錯誤] 無法取得主角圖片尺寸")
except Exception as e:
    fighter_img = None
    print(f"[主角圖片載入失敗] {e}")

# 設定主角移動速度
fighter_speed = 5  # 每次按鍵移動5像素

while True:  # 進入主遊戲迴圈，持續執行直到程式結束
    clock.tick(200)  # 設定每秒最多執行200次迴圈（FPS=200），控制遊戲速度
    for event in pygame.event.get():  # 取得所有事件（如鍵盤、滑鼠、關閉視窗等）
        if event.type == pygame.QUIT:  # 如果玩家按下關閉視窗按鈕
            pygame.quit()  # 關閉pygame
            sys.exit()  # 結束程式

    # ======================== 主角鍵盤移動 ========================
    # 取得目前所有按鍵的狀態
    keys = pygame.key.get_pressed()
    # 新增：根據移動方向切換主角圖片
    # 優先判斷左右鍵，若同時按下則以左為主
    if fighter_img_M:  # 若主角圖片有成功載入才允許移動
        if keys[pygame.K_LEFT]:
            fighter_img = (
                fighter_img_L if fighter_img_L else fighter_img_M
            )  # 左移時顯示左移圖
            fighter_x = max(0, fighter_x - fighter_speed)  # 左移，不能超出左邊界
        elif keys[pygame.K_RIGHT]:
            fighter_img = (
                fighter_img_R if fighter_img_R else fighter_img_M
            )  # 右移時顯示右移圖
            fighter_x = min(
                win_width - fighter_w, fighter_x + fighter_speed
            )  # 右移，不能超出右邊界
        else:
            fighter_img = fighter_img_M  # 沒有左右移動時顯示中立圖

        # 上下移動不影響圖片
        if keys[pygame.K_UP]:
            fighter_y = max(0, fighter_y - fighter_speed)  # 上移，不能超出上邊界
        if keys[pygame.K_DOWN]:
            fighter_y = min(
                win_height - fighter_h, fighter_y + fighter_speed
            )  # 下移，不能超出下邊界
    # ======================== 背景捲動繪製 ========================
    # 若成功載入背景圖片，則進行捲動繪製
    if bg_image:  # 如果背景圖片有成功載入
        # 1. 先繪製第一張背景，座標為 (0, bg_y)
        screen.blit(bg_image, (0, bg_y))  # 將背景圖片繪製在(0, bg_y)位置
        # 2. 再繪製第二張背景，座標為 (0, bg_y - 背景高度)，讓兩張圖片上下銜接
        screen.blit(
            bg_image, (0, bg_y - bg_image.get_height())
        )  # 在上一張上方再畫一張，實現無縫銜接
        # 3. 每次迴圈讓bg_y增加，背景向下捲動
        bg_y += bg_speed  # 背景y座標每次增加bg_speed，產生捲動效果
        # 4. 當第一張背景完全移出視窗時，重設bg_y為0，實現無縫循環
        if bg_y >= bg_image.get_height():  # 如果第一張背景完全移出視窗
            bg_y = 0  # 將y座標重設為0，循環捲動
    else:
        # 若背景圖片載入失敗，則以黑色填滿視窗
        screen.fill((0, 0, 0))  # 將整個視窗填滿黑色

    # ======================== 主角繪製 ========================
    # 將主角圖片繪製在目前座標
    # 根據目前方向顯示對應圖片
    if fighter_img:
        screen.blit(
            fighter_img, (fighter_x, fighter_y)
        )  # 將主角繪製在(fighter_x, fighter_y)
    pygame.display.update()  # 更新畫面，顯示所有繪製內容
