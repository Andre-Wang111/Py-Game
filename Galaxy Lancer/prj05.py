###################### 載入套件 ######################
import pygame  # 匯入pygame模組，負責遊戲視覺、音效等功能
import sys  # 匯入sys模組，提供系統相關功能（如取得執行路徑、結束程式）
import os  # 匯入os模組，負責檔案與目錄操作
import random  # 匯入random模組，用於隨機產生敵人位置/類型

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
clock = pygame.time.Clock()  # 建立一個Clock物件，用來控制遊戲迴圈的執行速度（FPS）#！


###################### 載入背景圖片 ######################
try:
    bg_path = os.path.join("image", "space.png")
    # 組合背景圖片的路徑（image/space.png）
    if os.path.exists(bg_path):  # 檢查背景圖片檔案是否存在
        bg_image = pygame.image.load(bg_path).convert()
        # 載入背景圖片並轉換為適合顯示的格式
        print(f"[載入成功] {bg_path}")  # 印出載入成功訊息
        # 取得圖片原始尺寸，並將視窗設為3/4
        img_width = bg_image.get_width()  # 取得背景圖片的寬度
        img_height = bg_image.get_height()  # 取得背景圖片的高度
        win_width = int(img_width * 0.75)  # 將視窗寬度設為圖片寬度的3/4
        win_height = int(img_height * 0.75)  # 將視窗高度設為圖片高度的3/4
        win_size = (win_width, win_height)  # 更新視窗尺寸
        # 取得螢幕解析度，計算置中座標
        screen = pygame.display.set_mode(win_size)  # 重新建立新尺寸的視窗
    else:
        bg_image = None  # 若找不到圖片，設為None
        print(f"[找不到圖片] {bg_path}")  # 印出找不到圖片的訊息
except Exception as e:
    bg_image = None  # 若載入過程發生例外，設為None
    print(f"[背景圖片載入失敗] {e}")  # 印出錯誤訊息
import os  # 確保可以使用os模組進行檔案操作

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

# ======================== 載入飛船尾焰圖片 (starship_burner) ========================
# 嘗試載入顯示在飛船尾部的焰火圖片，檔案位於 image/starship_burner.png
try:
    burner_path = os.path.join("image", "starship_burner.png")  # 建立尾焰圖片路徑
    if os.path.exists(burner_path):  # 檢查尾焰圖片是否存在
        # 載入原始尾焰圖片並保留 alpha 通道
        burner_img = pygame.image.load(burner_path).convert_alpha()
        print(f"[載入成功] {burner_path}")  # 印出載入成功訊息
        # 取得原始尾焰尺寸，之後用於建立動畫幀
        orig_burner_w = burner_img.get_width()  # 原始尾焰寬度
        orig_burner_h = burner_img.get_height()  # 原始尾焰高度

        # 建立尾焰動畫幀（使用不同縮放比例製作簡單動畫效果）
        burner_frames = []  # 儲存各動畫幀的表面
        # 使用一組縮放比例來模擬閃爍/膨脹的火焰動畫
        frame_scales = [
            0.75,
            1.0,
            1.2,
            1.0,
        ]  # 動畫幀的縮放比例（可調整以改變動畫速率/幅度）
        for scale in frame_scales:
            # 計算縮放後的尺寸
            fw = max(1, int(orig_burner_w * scale))  # 確保寬度至少為1
            fh = max(1, int(orig_burner_h * scale))  # 確保高度至少為1
            # 使用 smoothscale 以獲得較好的縮放品質
            frame = pygame.transform.smoothscale(burner_img, (fw, fh))
            burner_frames.append(frame)  # 將縮放後的幀加入列表

        # 初始化動畫索引與計時器，用於每幀更新
        burner_frame_index = 0  # 當前顯示的動畫幀索引
        burner_frame_delay = 4  # 每幾個遊戲循環切換一次幀（數字越小動畫越快）
        burner_frame_counter = 0  # 計數器，累積到 delay 來推進幀索引
    else:
        # 若沒有找到尾焰圖片，將相關變數初始化為安全的預設值
        burner_img = None  # 沒有原始圖片
        burner_frames = []  # 空的動畫幀列表
        burner_frame_index = 0
        burner_frame_delay = 1
        burner_frame_counter = 0
        orig_burner_w = orig_burner_h = 0
        print(f"[找不到圖片] {burner_path}")  # 印出找不到尾焰圖片訊息
except Exception as e:
    # 發生例外時將所有尾焰相關資源設定成安全的預設值，並印出錯誤訊息
    burner_img = None
    burner_frames = []
    burner_frame_index = 0
    burner_frame_delay = 1
    burner_frame_counter = 0
    orig_burner_w = orig_burner_h = 0
    print(f"[尾焰圖片載入失敗] {e}")  # 印出尾焰載入失敗的錯誤訊息

# 設定主角移動速度
fighter_speed = 5  # 每次按鍵移動5像素

# ======================== 載入子彈圖片與子彈管理 ========================
try:
    # bullet 圖片相對路徑（image/bullet.png）
    bullet_path = os.path.join("image", "bullet.png")
    if os.path.exists(bullet_path):
        # 載入子彈圖片並保留 alpha 通道以支援透明背景
        bullet_img = pygame.image.load(bullet_path).convert_alpha()
        print(f"[載入成功] {bullet_path}")
    else:
        bullet_img = None  # 若找不到檔案則設為 None
        print(f"[找不到圖片] {bullet_path}")
except Exception as e:
    bullet_img = None
    print(f"[子彈圖片載入失敗] {e}")

# 儲存活躍子彈的列表，每個子彈為 dict: {x, y, vx, vy, img}
bullets = []
# 子彈速度（像素/幀）
bullet_speed = 10

# ======================== 新增：載入/產生 敵人圖片與初始化參數 ========================
# 嘗試載入 image/enemy1.png 與 image/enemy2.png，若不存在則建立簡單的 placeholder
try:
    # 敵人圖片路徑
    enemy1_path = os.path.join("image", "enemy1.png")  # enemy1 檔案路徑
    enemy2_path = os.path.join("image", "enemy2.png")  # enemy2 檔案路徑

    # 先預設為 None，載入成功會放入 pygame.Surface
    enemy_img1 = enemy_img2 = None

    # 如果檔案存在，直接載入並保留 alpha 通道
    if os.path.exists(enemy1_path):
        enemy_img1 = pygame.image.load(enemy1_path).convert_alpha()  # 載入 enemy1
        print(f"[載入成功] {enemy1_path}")
    else:
        # 建立一個簡單的紅色方塊作為 placeholder（包含 alpha）
        placeholder1 = pygame.Surface(
            (40, 30), pygame.SRCALPHA
        )  # 建立有 alpha 的 Surface
        placeholder1.fill((200, 30, 30, 255))  # 用紅色填滿作為占位圖
        try:
            pygame.image.save(placeholder1, enemy1_path)  # 嘗試儲存成 image/enemy1.png
            enemy_img1 = pygame.image.load(
                enemy1_path
            ).convert_alpha()  # 再載入以統一處理
            print(f"[已建立 placeholder 並載入] {enemy1_path}")
        except Exception:
            # 儲存失敗時，仍使用記憶體上的 Surface
            enemy_img1 = placeholder1
            print(f"[警告] 無法儲存 {enemy1_path}，使用記憶體 placeholder")

    if os.path.exists(enemy2_path):
        enemy_img2 = pygame.image.load(enemy2_path).convert_alpha()  # 載入 enemy2
        print(f"[載入成功] {enemy2_path}")
    else:
        # 建立藍色方塊作為 placeholder
        placeholder2 = pygame.Surface(
            (36, 28), pygame.SRCALPHA
        )  # 建立有 alpha 的 Surface
        placeholder2.fill((30, 120, 200, 255))  # 用藍色填滿作為占位圖
        try:
            pygame.image.save(placeholder2, enemy2_path)  # 嘗試儲存成 image/enemy2.png
            enemy_img2 = pygame.image.load(enemy2_path).convert_alpha()  # 再載入
            print(f"[已建立 placeholder 並載入] {enemy2_path}")
        except Exception:
            enemy_img2 = placeholder2
            print(f"[警告] 無法儲存 {enemy2_path}，使用記憶體 placeholder")
except Exception as e:
    # 若發生任何例外，確保變數都有合理預設值以避免後續錯誤
    enemy_img1 = enemy_img1 if "enemy_img1" in globals() else None
    enemy_img2 = enemy_img2 if "enemy_img2" in globals() else None
    print(f"[敵人圖片處理失敗] {e}")

# ======================== 新增：載入爆炸動畫素材與初始化爆炸管理 ========================
# 嘗試載入 5 張爆炸圖片 (explosion1.png ~ explosion5.png)，若不存在則建立簡單的佔位圖片並儲存
try:
    # 建立要載入的爆炸圖片路徑清單（從 1 到 5）
    explosion_paths = [os.path.join("image", f"explosion{i}.png") for i in range(1, 6)]
    explosion_frames = []  # 用來儲存每一幀的 pygame.Surface
    # 逐一檢查每張圖片是否存在，若存在就載入，否則建立一張簡單的圓形爆炸佔位圖並儲存後再載入
    for idx, p in enumerate(explosion_paths):
        if os.path.exists(p):
            # 若檔案存在，直接載入並保留 alpha 通道
            explosion_frames.append(pygame.image.load(p).convert_alpha())
            print(f"[載入成功] {p}")
        else:
            # 建立一個簡單的漸層圓形作為佔位爆炸圖，尺寸隨索引變化以模擬不同幀
            size = 24 + idx * 8  # 依索引放大尺寸，讓幀看起來有變化
            placeholder = pygame.Surface(
                (size, size), pygame.SRCALPHA
            )  # 建立有 alpha 的 Surface
            # 填滿透明背景
            placeholder.fill((0, 0, 0, 0))
            # 畫一個圓形，從黃色到紅色漸層可以用不同顏色模擬
            color = (255, max(50, 255 - idx * 30), 0, 220)  # 由黃到橙到紅
            pygame.draw.circle(placeholder, color, (size // 2, size // 2), size // 2)
            try:
                # 嘗試將佔位圖儲存為檔案，方便未來編輯或替換為真實素材
                pygame.image.save(placeholder, p)
                explosion_frames.append(pygame.image.load(p).convert_alpha())
                print(f"[已建立佔位爆炸圖並載入] {p}")
            except Exception:
                # 若無法儲存，仍然使用記憶體上的 Surface 當作動畫幀
                explosion_frames.append(placeholder)
                print(f"[警告] 無法儲存 {p}，使用記憶體佔位圖")
except Exception as e:
    # 若載入爆炸素材失敗，確保變數有預設值以免後續發生錯誤
    explosion_frames = explosion_frames if "explosion_frames" in globals() else []
    print(f"[爆炸圖片處理失敗] {e}")

# 儲存目前畫面上所有爆炸動畫的列表，每個爆炸為 dict: {x, y, frames, index, delay, counter}
explosions = []

# 敵人清單與行為參數
enemies = []  # 儲存目前畫面/場景中所有敵人，每個物件為 dict: {x, y, vx, vy, img}
enemy_base_speed = 1  # 敵人自身向下移動速度（像素/幀）
enemy_spawn_delay = 120  # 產生敵人的間隔（frames）
enemy_spawn_counter = 0  # 產生計數器


while True:  # 進入主遊戲迴圈，持續執行直到程式結束
    clock.tick(200)  # 設定每秒最多執行200次迴圈（FPS=200），控制遊戲速度
    for event in pygame.event.get():  # 取得所有事件（如鍵盤、滑鼠、關閉視窗等）
        if event.type == pygame.QUIT:  # 如果玩家按下關閉視窗按鈕
            pygame.quit()  # 關閉pygame
            sys.exit()  # 結束程式
        # 處理按鍵按下事件，這裡用來偵測空白鍵發射子彈
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # 當玩家按下空白鍵時
                # 僅在子彈圖片與飛船圖片皆存在時才能發射
                if bullet_img and fighter_img:
                    # 取得子彈尺寸以計算出生位置
                    bw = bullet_img.get_width()
                    bh = bullet_img.get_height()

                    # 根據主角目前顯示的圖片決定子彈發射方向與出生位置
                    if fighter_img == fighter_img_L:
                        # 飛船面向左：子彈從飛船左側發射，垂直置中
                        bx = fighter_x - bw
                        by = fighter_y + (fighter_h - bh) // 2
                        vx, vy = -bullet_speed, 0
                    elif fighter_img == fighter_img_R:
                        # 飛船面向右：子彈從飛船右側發射，垂直置中
                        bx = fighter_x + fighter_w
                        by = fighter_y + (fighter_h - bh) // 2
                        vx, vy = bullet_speed, 0
                    else:
                        # 飛船中立（面向上）：子彈從飛船上方發射，水平置中
                        bx = fighter_x + (fighter_w - bw) // 2
                        by = fighter_y - bh
                        vx, vy = 0, -bullet_speed

                    # 建立子彈物件並加入 bullets 列表進行管理
                    bullets.append(
                        {"x": bx, "y": by, "vx": vx, "vy": vy, "img": bullet_img}
                    )

    # ======================== 主角鍵盤移動 ========================
    # 取得目前所有按鍵的狀態
    keys = pygame.key.get_pressed()
    # 新增：根據移動方向切換主角圖片
    # 優先判斷左右鍵，若同時按下則以左為主
    if fighter_img_M:  # 若主角圖片有成功載入才允許移動
        if keys[pygame.K_LEFT]:
            fighter_img = fighter_img_L if fighter_img_L else fighter_img_M
            # 左移時顯示左移圖  #條件在中間，成功在左邊，失敗在右邊
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

    # ======================== 新增：敵人產生、移動與繪製 ========================
    # 每一幀都要更新敵人計時器，並在到達 spawn 間隔時產生新敵人
    enemy_spawn_counter += 1  # 敵人產生計數器每幀遞增
    if enemy_spawn_counter >= enemy_spawn_delay:  # 若累積到達產生延遲
        enemy_spawn_counter = 0  # 重設計數器
        # 選擇敵人圖像（若兩張都存在就隨機選一張）
        chosen_img = None  # 先預設為 None
        if enemy_img1 and enemy_img2:
            chosen_img = random.choice([enemy_img1, enemy_img2])  # 隨機挑選一張敵人圖片
        elif enemy_img1:
            chosen_img = enemy_img1
        elif enemy_img2:
            chosen_img = enemy_img2

        if chosen_img:  # 只有當有可用的敵人圖片時才建立敵人
            ew = chosen_img.get_width()  # 取得敵人寬度以避免生成位置超出畫面
            eh = chosen_img.get_height()  # 取得敵人高度
            ex = random.randint(
                0, max(0, win_width - ew)
            )  # 隨機 x 位置，保證不會超出右邊界
            ey = -eh - random.randint(0, 40)  # 產生在畫面上方稍遠處，讓敵人從上方出現
            # 建立敵人物件 dict，包含位置、速度與圖像
            enemies.append(
                {"x": ex, "y": ey, "vx": 0, "vy": enemy_base_speed, "img": chosen_img}
            )

    # 更新並繪製所有敵人：敵人的 y 會受自身速度與背景捲動速度影響
    if enemies:  # 只有在有敵人時才進行更新與繪製
        new_enemies = []  # 用於儲存仍在畫面範圍內的敵人
        for e in enemies:
            # 更新敵人位置：自身垂直速度 + 背景滾動速度，讓敵人會跟著畫面捲動
            e["x"] += e.get("vx", 0)  # 橫向速度影響 x
            e["y"] += e.get("vy", 0) + bg_speed  # 垂直速度加上背景捲動速度
            # 若敵人仍在畫面附近範圍，則保留並繪製
            if -100 <= e["x"] <= win_width + 100 and -100 <= e["y"] <= win_height + 100:
                new_enemies.append(e)  # 加入新的敵人列表以保留
                try:
                    screen.blit(e["img"], (int(e["x"]), int(e["y"])))  # 繪製敵人
                except Exception:
                    # 若繪製失敗（例如圖像為 None），則忽略該次繪製
                    pass
            # 超出範圍的敵人會自動被丟棄（不加入 new_enemies）
        enemies = new_enemies  # 更新敵人清單為仍然活躍的敵人

    # ======================== 主角繪製 ========================
    # 將主角圖片繪製在目前座標
    # 根據目前方向顯示對應圖片
    # 新增：決定是否顯示尾焰（規則：當玩家往下移動時不顯示尾焰，其餘情況皆顯示）
    # ------------------------ 子彈更新與繪製 ------------------------
    # 每一幀都要更新子彈位置，並在畫面上繪製所有活躍子彈
    if bullets:  # 只有當有活躍子彈時才執行以下迴圈
        # 使用索引迭代並建立新的列表以移除越界的子彈
        new_bullets = []  # 用於暫存仍在畫面內的子彈
        # 當前迴圈若發生子彈擊中敵人的情況，記錄要移除的敵人清單 (以物件為準)
        enemies_to_remove = []  # 儲存被擊中的敵人以便在後續移除
        for b in bullets:
            # 更新子彈位置：x 與 y 加上速度分量
            b["x"] += b["vx"]  # 橫向位移
            b["y"] += b["vy"]  # 縱向位移
            # 判斷子彈是否仍在畫面範圍內（若在則保留並繪製）
            if -50 <= b["x"] <= win_width + 50 and -50 <= b["y"] <= win_height + 50:
                # 檢查此子彈是否擊中任一敵人：以簡單矩形碰撞判定
                hit = False  # 記錄此子彈是否已命中敵人
                try:
                    # 建立子彈的矩形用於碰撞偵測
                    b_rect = b["img"].get_rect(topleft=(int(b["x"]), int(b["y"])))
                except Exception:
                    # 若子彈圖片不存在則跳過碰撞檢查
                    b_rect = None

                if b_rect and enemies:
                    for e in enemies:
                        try:
                            # 建立敵人的矩形用於碰撞偵測
                            e_rect = e["img"].get_rect(
                                topleft=(int(e["x"]), int(e["y"]))
                            )
                        except Exception:
                            # 若敵人圖片不存在則略過此敵人
                            continue
                        # 若矩形相交，視為命中
                        if b_rect.colliderect(e_rect):
                            hit = True  # 標記子彈已命中
                            # 建立一個爆炸物件放在敵人中心位置，並儲存動畫幀與計時資訊
                            explosions.append(
                                {
                                    "x": int(e["x"] + e["img"].get_width() // 2),
                                    "y": int(e["y"] + e["img"].get_height() // 2),
                                    "frames": explosion_frames,  # 爆炸幀清單
                                    "index": 0,  # 當前顯示的動畫幀索引
                                    "delay": 2,  # 每幾個循環切換一次幀（數字越小動畫越快）
                                    "counter": 0,  # 計數器用於累積到 delay
                                }
                            )
                            # 將被命中的敵人加入移除清單，避免後續繼續繪製或被再次命中
                            enemies_to_remove.append(e)
                            break  # 一顆子彈只會擊中一個敵人，跳出敵人迴圈

                if not hit:
                    # 若沒有命中，則保留此子彈並在畫面上繪製
                    new_bullets.append(b)
                    try:
                        screen.blit(b["img"], (int(b["x"]), int(b["y"])))
                    except Exception:
                        # 若繪製失敗（例如圖面為 None），忽略該次繪製
                        pass
            # 若子彈超出邊界，則不加入 new_bullets，等同於移除子彈
        bullets = new_bullets  # 更新活躍子彈列表
        # 若有敵人在本幀被擊中，從 enemies 中移除這些敵人
        if enemies_to_remove:
            enemies = [e for e in enemies if e not in enemies_to_remove]

    # ======================== 新增：爆炸動畫更新與繪製 ========================
    # 在子彈與敵人處理之後，更新並繪製目前所有的爆炸動畫
    if explosions:  # 只有在爆炸列表非空時才進行更新
        new_explosions = []  # 用於儲存尚未播放完畢的爆炸動畫
        for ex in explosions:
            # 取得動畫幀清單（可能為空）並檢查是否可用
            frames = ex.get("frames", [])
            if not frames:
                # 若沒有幀，則略過此爆炸（不再保留）
                continue
            # 取得當前要繪製的幀並計算其圖像左上角，以便讓爆炸以中心為基準顯示
            cur_frame = frames[ex["index"]]
            fw = cur_frame.get_width()
            fh = cur_frame.get_height()
            fx = int(ex["x"] - fw // 2)  # 將爆炸圖片水平置中於爆炸座標
            fy = int(ex["y"] - fh // 2)  # 將爆炸圖片垂直置中於爆炸座標
            try:
                screen.blit(cur_frame, (fx, fy))  # 在畫面上繪製當前幀
            except Exception:
                # 若繪製失敗則忽略
                pass

            # 更新動畫計時器，累積到 delay 後推進到下一個幀
            ex["counter"] += 1
            if ex["counter"] >= ex["delay"]:
                ex["counter"] = 0
                ex["index"] += 1
            # 若索引尚未超過最後一幀，則保留動畫繼續顯示
            if ex["index"] < len(frames):
                new_explosions.append(ex)
            # 當索引已超過最後一幀時，不再加入 new_explosions（代表動畫結束）
        explosions = new_explosions  # 更新爆炸清單為仍在播放的動畫

    # ======================== 主角繪製 ========================
    # 將主角圖片繪製在目前座標
    # 根據目前方向顯示對應圖片
    # 新增：決定是否顯示尾焰（規則：當玩家往下移動時不顯示尾焰，其餘情況皆顯示）
    if fighter_img:  # 只有在主角圖片存在時才進行尾焰繪製判斷與繪製
        show_burner = True  # 預設顯示尾焰（包含靜止與往左/右/上移動）
        if keys[pygame.K_DOWN]:  # 若玩家正在按下向下鍵，代表往後移動
            show_burner = False  # 往後移動時不顯示尾焰

        # 若有成功建立尾焰動畫幀並且判斷需要顯示尾焰，則先繪製目前動畫幀於飛船尾部
        if burner_frames and show_burner:
            # 取得當前動畫幀（surface）並計算其尺寸以做正確定位
            frame = burner_frames[burner_frame_index]  # 取出當前索引的幀
            fw = frame.get_width()  # 當前幀寬度
            fh = frame.get_height()  # 當前幀高度
            # 計算尾焰繪製位置：水平置中於飛船圖片底部，並稍微向下偏移以產生重疊感
            # 為了讓尾焰能隨不同方向的飛機圖（左右/中立）正確置中，使用當前顯示的 fighter_img
            cur_fighter_w = fighter_img.get_width() if fighter_img else fighter_w
            cur_fighter_h = fighter_img.get_height() if fighter_img else fighter_h
            burner_x = (
                fighter_x + (cur_fighter_w - fw) // 2
            )  # 尾焰水平置中於目前顯示的主角圖
            burner_y = fighter_y + fighter_h - (fh // 4)  # 尾焰位於主角下方一小段距離
            screen.blit(frame, (burner_x, burner_y))  # 在計算好的位置繪製當前動畫幀

            # 更新動畫計時器：每 accum 到 delay 就切換下一個幀
            burner_frame_counter += 1  # 動畫計數器遞增
            if burner_frame_counter >= burner_frame_delay:  # 若達到切換延遲
                burner_frame_counter = 0  # 重設計數器
                # 推進幀索引，模循環播放
                burner_frame_index = (burner_frame_index + 1) % len(burner_frames)

        # 最後繪製主角，確保主角在尾焰之上，看起來尾焰是從飛船尾端發出
        screen.blit(
            fighter_img, (fighter_x, fighter_y)
        )  # 將主角繪製在(fighter_x, fighter_y)
    pygame.display.update()  # 更新畫面，顯示所有繪製內容
