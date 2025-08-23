###################### 載入套件 #######################
import pygame  # 遊戲主程式套件
import sys  # 系統相關功能（如結束程式）
import os  # 處理路徑用
import random  # 用於產生敵人隨機 X 位置與隨機選圖

###################### 初始化設定 #######################
pygame.init()  # 初始化 pygame(把程式打開)
FPS = pygame.time.Clock()  # 設定 FPS 時脈
# --------------- 新增 子彈與火焰的資料結構 ---------------
###################### 載入背景圖片 #######################
# 設定圖片路徑
base_dir = os.path.dirname(os.path.abspath(__file__))  # 取得目前檔案所在資料夾
# 圖片資料夾路徑：使用與此檔案同一資料夾下的 `image` 子資料夾
# 原本使用上層路徑會導致找不到放在 `Galaxy Lancer/image` 內的資源，
# 因此改為指向本資料夾的 image 子資料夾。
image_dir = os.path.join(base_dir, "image")  # 圖片資料夾路徑（同目錄下的 image）
bg_path = os.path.join(image_dir, "space.png")  # 背景圖片完整路徑

# 載入圖片
bg_img = pygame.image.load(bg_path)  # 載入背景圖片
bg_width, bg_height = bg_img.get_width(), bg_img.get_height()  # 取得圖片寬高

# ====================== 背景捲動參數 ======================
# 設定背景圖片的初始 y 座標
bg_y1 = 0  # 第一張圖片的 y 座標
bg_y2 = -bg_height  # 第二張圖片的 y 座標（接在第一張上方）
scroll_speed = 10  # 捲動速度（每幀向上移動的像素數）
# 說明：scroll_speed 設為 10，代表每秒 60 幀時，背景每幀會向上移動 10 像素，
# 即每秒移動 600 像素，符合「一次十格每秒60幀」的需求。

# 設定視窗大小與標題
screen = pygame.display.set_mode((bg_width, bg_height))  # 視窗大小與圖片相同
pygame.display.set_caption("Space Background Scroll")  # 視窗標題

# ====================== 載入飛船圖片與初始參數 ======================

# ====================== 載入飛船圖片（左右方向） ======================
# 載入三種飛船圖片：預設（中）、左、右
# fighter_img_M：預設靜止或垂直移動時顯示
# fighter_img_L：往左移動時顯示
# fighter_img_R：往右移動時顯示
fighter_img_M = pygame.image.load(
    os.path.join(image_dir, "fighter_M.png")
)  # 預設飛船圖片
fighter_img_L = pygame.image.load(
    os.path.join(image_dir, "fighter_L.png")
)  # 左移飛船圖片
fighter_img_R = pygame.image.load(
    os.path.join(image_dir, "fighter_R.png")
)  # 右移飛船圖片

# 預設顯示中間飛船（靜止或上下移動時）
fighter_img = fighter_img_M
fighter_rect = fighter_img.get_rect()  # 取得飛船矩形區域

# 設定飛船初始位置（畫面中央下方）
fighter_rect.centerx = bg_width // 2  # 水平置中
fighter_rect.bottom = bg_height - 30  # 距離底部 30 像素

# 設定飛船初始速度
fighter_speed_x = 0  # 水平速度
fighter_speed_y = 0  # 垂直速度
fighter_move_speed = 8  # 飛船移動速度（每次按鍵移動的像素數）
# 載入子彈圖片與相關參數
bullet_img = pygame.image.load(os.path.join(image_dir, "bullet.png"))  # 子彈圖片
bullets = []  # 子彈清單，儲存每個子彈物件（Bullet 類別的實例）
bullet_speed = -15  # 子彈垂直速度（向上），負值代表往上移動

# ====================== 載入敵人圖片與參數 ======================
# 載入兩種敵人圖片，供生成時隨機挑選
enemy_img_1 = pygame.image.load(os.path.join(image_dir, "enemy1.png"))  # 敵人圖片1
enemy_img_2 = pygame.image.load(os.path.join(image_dir, "enemy2.png"))  # 敵人圖片2
enemy_images = [enemy_img_1, enemy_img_2]  # 敵人圖片清單（供隨機取用）
enemies = []  # 敵人清單，儲存 Enemy 物件
enemy_speed = 6  # 敵人垂直速度（像素/幀），正值代表向下
spawn_timer = 0  # 生成計時器（單位：幀）
spawn_interval = 60  # 生成間隔（幀數），60 幀約等於 1 秒（60 FPS）

# ================ 載入爆炸動畫圖片（五張） ================
# 依序載入 explosion1..explosion5，並儲存在一個清單中供 Explosion 類別使用
explosion_imgs = [
    pygame.image.load(os.path.join(image_dir, "explosion1.png")),
    pygame.image.load(os.path.join(image_dir, "explosion2.png")),
    pygame.image.load(os.path.join(image_dir, "explosion3.png")),
    pygame.image.load(os.path.join(image_dir, "explosion4.png")),
    pygame.image.load(os.path.join(image_dir, "explosion5.png")),
]

# 儲存目前所有正在播放的爆炸動畫實例
explosions = []  # Explosion 物件清單

# ----------------- 新增玩家血量與碰撞後無敵/閃爍狀態變數 -----------------
player_hp = 100  # 玩家初始血量為 100（表示 100 滴血）
invulnerable = False  # 是否處於無敵狀態（碰撞後短暫無敵以避免連續受傷）
invuln_timer = 0  # 無敵狀態計時器（以幀數為單位）
invuln_duration = 60  # 無敵持續時間，60 幀約等於 1 秒（60 FPS）
flash_counter = 0  # 用於控制閃爍顯示的計數器
game_over = False  # 當血量歸零時切換為 True，顯示結束畫面

# 新增玩家分數變數：分數在遊戲過程中累積，擊敗敵人時會增加
# 初始分數設為 0（整數），每擊敗一個敵人會加 10
score = 0  # 玩家目前分數

# ----------------- 新增能量（Energy）相關變數 -----------------
# 能量系統：最大能量、目前能量、每次發射消耗、回復量與回復間隔
energy_max = 10  # 能量上限為 10
energy = energy_max  # 當前能量值，初始為滿
energy_cost_per_shot = 1  # 每發子彈消耗能量數
energy_regen_amount = 2  # 每次回復的能量數
energy_regen_interval_ms = 5000  # 能量回復間隔（毫秒），設定為 5000ms = 5 秒
# 使用 pygame 的時間（毫秒）來追蹤上一次回復的時間點
last_energy_regen_time = (
    pygame.time.get_ticks()
)  # 紀錄上次回復能量的時間（初始化為現在）
# ----------------- 新增血量回復系統變數 -----------------
# health_regen_amount: 每次血量回復的數值（此處設定為 20 點）
health_regen_amount = 20  # 每次回復 20 點血量（新增變數，詳述回復值）
# health_regen_interval_ms: 血量回復的時間間隔（毫秒），此處設定為 10000ms = 10 秒
health_regen_interval_ms = 10000  # 設定為 10 秒一次回復（毫秒）
# last_health_regen_time: 使用 pygame.time.get_ticks() 記錄上一次回復血量的時間戳（毫秒）
last_health_regen_time = pygame.time.get_ticks()  # 初始設定為現在的時間（防止馬上回復）

# 載入遊戲結束畫面圖片（血量為 0 時顯示）
gameover_img = pygame.image.load(os.path.join(image_dir, "gameover (1).png"))


# ----------------- 定義子彈類別 -----------------
class Bullet:
    """
    Bullet 物件管理單一顆子彈的狀態與行為

    屬性：
    - image: 子彈圖片 Surface
    - rect: Pygame Rect，表示子彈在畫面上的位置與大小
    - speed_y: 垂直速度（像素/幀），負值代表向上

    方法：
    - update(): 根據速度更新位置
    - draw(surface): 在指定的 surface 上繪製子彈
    - off_screen(): 判斷子彈是否已經離開畫面（頂端之外）
    """

    def __init__(self, image, x, y, speed_y):
        # 儲存圖片與速度參數
        self.image = image  # 子彈圖片 Surface
        self.rect = self.image.get_rect()  # 由圖片建立 rect（定位用）
        # 設定子彈初始位置：以傳入的 x, y 為中心或底端位置
        self.rect.centerx = x  # 子彈水平置中
        self.rect.bottom = y  # 子彈底部對齊傳入的 y（通常為飛機頂端）
        self.speed_y = speed_y  # 子彈垂直速度（像素/幀）

    def update(self):
        """根據速度更新子彈位置（每幀呼叫）。"""
        self.rect.y += self.speed_y  # 更新 y 座標（向上或向下）

    def draw(self, surface):
        """在指定的 surface（通常為 screen）上繪製子彈。"""
        surface.blit(self.image, self.rect)

    def off_screen(self):
        """回傳 True 表示子彈已離開畫面（在頂端之外），否則 False。"""
        return self.rect.bottom < 0


# ----------------- 定義敵人類別 -----------------
class Enemy:
    """
    Enemy 物件管理單一個敵人的狀態與行為

    屬性：
    - image: 敵人圖片 Surface
    - rect: Pygame Rect，表示敵人在畫面上的位置與大小
    - speed_y: 垂直速度（像素/幀），正值代表往下

    方法：
    - update(): 根據速度更新位置
    - draw(surface): 在指定的 surface 上繪製敵人
    - off_screen(): 判斷敵人是否已經離開畫面（在底部之外）
    """

    def __init__(self, image, x, y, speed_y):
        self.image = image  # 儲存圖片 Surface
        self.rect = self.image.get_rect()  # 由圖片建立 rect（定位用）
        self.rect.x = x  # 設定水平座標（左上角為基準）
        self.rect.y = y  # 設定垂直座標（左上角為基準）
        self.speed_y = speed_y  # 儲存垂直速度（正值向下）

    def update(self):
        """每幀呼叫：根據垂直速度更新敵人位置。"""
        self.rect.y += self.speed_y  # y 座標增加（往下移動）

    def draw(self, surface):
        """在指定的 surface（通常為 screen）上繪製敵人。"""
        surface.blit(self.image, self.rect)  # 繪製敵人圖到畫面

    def off_screen(self):
        """若敵人已經從畫面底部離開，回傳 True，否則 False。"""
        return self.rect.top > bg_height  # top 大於畫面高度表示完全離開


# ----------------- 定義爆炸（Explosion）類別 -----------------
class Explosion:
    """
    Explosion 物件管理一個爆炸動畫的播放

    屬性：
    - frames: 爆炸每一幀的圖片清單（Surface）
    - rect: 用來定位爆炸動畫的 Rect（會以敵人中心對齊）
    - frame_index: 目前要顯示的幀索引
    - frame_delay: 每張圖應該維持的幀數（用來控制動畫速度）
    - counter: 計數器，用來在多幀之間延時

    方法：
    - update(): 推進動畫幀，回傳 True 表示動畫結束
    - draw(surface): 在指定 surface 上繪製目前的動畫幀
    """

    def __init__(self, frames, center_x, center_y, frame_delay=4):
        # 儲存所有幀的圖片（Surface）以及初始化動畫索引與計時器
        self.frames = frames  # 爆炸每一張圖片的 Surface 清單
        self.frame_index = 0  # 目前顯示的幀索引（從 0 開始）
        self.frame_delay = frame_delay  # 每張圖維持的遊戲幀數
        self.counter = 0  # 計數器，用於計算何時切換到下一幀

        # 使用第一張圖片建立 rect，以便取得寬高與做對齊
        self.image = self.frames[self.frame_index]  # 目前要顯示的圖片
        self.rect = self.image.get_rect()  # 根據圖片建立 rect
        # 把爆炸中心對齊到傳入的中心座標（通常是敵人的中心）
        self.rect.centerx = center_x
        self.rect.centery = center_y

    def update(self):
        """每幀呼叫：更新動畫進度，若播放完畢回傳 True（代表可移除）。"""
        self.counter += 1  # 增加計時器
        # 當計數器超過 frame_delay 時切換到下一張圖
        if self.counter >= self.frame_delay:
            self.counter = 0  # 重置計數器
            self.frame_index += 1  # 前進到下一張圖
            # 若尚未超出範圍，更新當前圖片
            if self.frame_index < len(self.frames):
                self.image = self.frames[self.frame_index]
            else:
                # 當所有幀播放完畢，回傳 True 表示動畫結束
                return True
        return False

    def draw(self, surface):
        """在指定的 surface 上繪製目前的動畫幀圖片。"""
        surface.blit(self.image, self.rect)


# 載入火焰（噴射器）圖片並設定位置偏移量
burner_img = pygame.image.load(
    os.path.join(image_dir, "starship_burner.png")
)  # 噴焰圖片
burner_offset_x = 0  # 火焰相對於飛機中心的水平偏移（視圖片可調整）
burner_offset_y = 10  # 火焰相對於飛機底部的垂直偏移（向下）

# ====================== 主遊戲迴圈 ======================
while True:
    FPS.tick(60)  # 控制遊戲執行速度為每秒 60 幀
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # 關閉視窗時結束程式
        # ====================== 監聽鍵盤事件 ======================
        # 按下鍵盤時設定速度與切換對應圖片
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                fighter_speed_x = -fighter_move_speed  # 左移
                fighter_img = fighter_img_L  # 切換為左移圖片
            elif event.key == pygame.K_RIGHT:
                fighter_speed_x = fighter_move_speed  # 右移
                fighter_img = fighter_img_R  # 切換為右移圖片
            elif event.key == pygame.K_UP:
                fighter_speed_y = -fighter_move_speed  # 上移
            elif event.key == pygame.K_DOWN:
                fighter_speed_y = fighter_move_speed  # 下移
            elif event.key == pygame.K_SPACE:
                # 按下空白鍵發射：先檢查是否有足夠能量，若足夠則建立子彈並扣除能量
                # 若能量不足，則不會發射（可以在未來加入音效或提示）
                if energy >= energy_cost_per_shot and not game_over:
                    # 建立新的子彈物件，位置以飛機頂端為發射點
                    new_bullet = Bullet(
                        bullet_img, fighter_rect.centerx, fighter_rect.top, bullet_speed
                    )
                    bullets.append(new_bullet)  # 把新的子彈物件加入清單
                    # 扣除能量（每發消耗固定數量）
                    energy -= energy_cost_per_shot
                    # 確保能量不會低於 0
                    if energy < 0:
                        energy = 0
        # 放開鍵盤時停止移動，恢復預設圖片（靜止或上下移動時）
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                fighter_speed_x = 0
                fighter_img = fighter_img_M  # 恢復預設圖片
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                fighter_speed_y = 0

    # 更新背景圖片的 y 座標，讓圖片持續向上捲動
    bg_y1 += scroll_speed
    bg_y2 += scroll_speed

    # 如果圖片完全離開視窗上方，將其移到另一張圖片上方，實現無縫循環
    if bg_y1 >= bg_height:
        bg_y1 = bg_y2 - bg_height
    if bg_y2 >= bg_height:
        bg_y2 = bg_y1 - bg_height

    # 繪製兩張背景圖片
    screen.blit(bg_img, (0, bg_y1))
    screen.blit(bg_img, (0, bg_y2))

    # ====================== 更新飛船位置 ======================
    fighter_rect.x += fighter_speed_x  # 更新水平位置
    fighter_rect.y += fighter_speed_y  # 更新垂直位置
    # 限制飛船不超出畫面範圍
    if fighter_rect.left < 0:
        fighter_rect.left = 0
    if fighter_rect.right > bg_width:
        fighter_rect.right = bg_width
    if fighter_rect.top < 0:
        fighter_rect.top = 0
    if fighter_rect.bottom > bg_height:
        fighter_rect.bottom = bg_height

    # ====================== 繪製飛船（延後至後段統一繪製以支援閃爍） ======================
    # 先不要在這裡繪製飛船與火焰，會在後段根據無敵/閃爍狀態統一繪製

    # 更新並繪製所有子彈：使用 Bullet 物件的方法，
    # 物件化可以將位置更新、繪製與狀態封裝在類別中
    for b in bullets[:]:  # 使用淺複製以便在迴圈中安全地移除元素
        b.update()  # 更新子彈位置（物件內部處理）
        b.draw(screen)  # 繪製子彈到畫面
        # 若子彈已離開畫面（在頂端之外），就從清單中移除
        if b.off_screen():
            bullets.remove(b)

    # ------------------ 子彈與敵人碰撞檢查（提前處理） ------------------
    # 將子彈與敵人的碰撞檢查放在敵人更新與玩家碰撞檢查之前，
    # 確保若敵人在此幀被子彈擊中並移除，不會再被同一幀的玩家碰撞判定傷害到玩家。
    # 這能解決：當敵人同時被子彈擊中與與玩家接觸時導致玩家誤受傷與閃爍的問題。
    for b in bullets[:]:  # 使用淺複製避免迭代時修改原清單
        for e in enemies[:]:
            # 使用 rect 的碰撞檢查函式 colliderect
            if b.rect.colliderect(e.rect):
                # 計算爆炸中心位置（以敵人中心為基準）
                ex_center_x = e.rect.centerx
                ex_center_y = e.rect.centery
                # 建立 Explosion，frame_delay 設為 4（可調整速度）
                new_explosion = Explosion(explosion_imgs, ex_center_x, ex_center_y, 4)
                explosions.append(new_explosion)  # 加入正在播放的爆炸清單

                # 碰撞發生：移除子彈與敵人以達到消失效果
                if b in bullets:
                    bullets.remove(b)
                if e in enemies:
                    enemies.remove(e)
                    # 擊敗敵人時增加分數：每個敵人固定加 10 分
                    # 使用全域 score 變數來累積玩家分數
                    score += 10  # 分數增加 10
                # 該子彈已被移除，跳出敵人迴圈並處理下一顆子彈
                break

    # ------------------ 敵人生成邏輯（每隔一段時間從上方向下） ------------------
    # 計時器增加（每幀累計）
    spawn_timer += 1  # 每一幀加 1，當達到 spawn_interval 時生成敵人
    if spawn_timer >= spawn_interval:
        # 生成一個新的敵人：隨機選擇一個圖片，並在畫面上方一開始的位置生成
        chosen_img = random.choice(enemy_images)  # 隨機選圖
        # 取得圖片寬度，避免敵人生成在畫面外
        img_w = chosen_img.get_width()
        # 計算敵人初始 x 座標：在 [0, bg_width - img_w] 範圍內隨機
        start_x = random.randint(0, max(0, bg_width - img_w))
        # 初始 y 座標放在畫面上方（負值，讓敵人從畫面外慢慢進入）
        start_y = -chosen_img.get_height()
        # 建立 Enemy 並加入敵人清單
        new_enemy = Enemy(chosen_img, start_x, start_y, enemy_speed)
        enemies.append(new_enemy)
        spawn_timer = 0  # 重置生成計時器

    # 更新並繪製所有敵人
    for e in enemies[:]:  # 使用淺複製以便安全移除
        e.update()  # 更新敵人位置（向下）
        e.draw(screen)  # 繪製敵人到畫面
        # 若敵人完全離開畫面底部，則從清單移除
        if e.off_screen():
            enemies.remove(e)

        # ------------------ 玩家與敵人碰撞檢查 ------------------
        # 若玩家與敵人發生碰撞，則產生爆炸、讓敵人消失，並讓玩家受傷
        if fighter_rect.colliderect(e.rect) and not invulnerable and not game_over:
            # 建立爆炸效果在敵人中心
            ex_center_x = e.rect.centerx
            ex_center_y = e.rect.centery
            new_explosion = Explosion(explosion_imgs, ex_center_x, ex_center_y, 4)
            explosions.append(new_explosion)

            # 從敵人清單移除該敵人（敵人消失）
            if e in enemies:
                enemies.remove(e)

            # 玩家受到傷害：扣 20 血
            player_hp -= 20
            # 若血量降到 0 或以下，設定遊戲結束狀態
            if player_hp <= 0:
                player_hp = 0
                game_over = True

            # 啟動短暫無敵與閃爍機制，避免連續受傷
            invulnerable = True
            invuln_timer = 0
            flash_counter = 0

    # (已在更新子彈後進行子彈與敵人的碰撞檢查，故此處移除重複程式以避免重複處理)

    # ------------------ 更新並繪製所有爆炸動畫 ------------------
    for ex in explosions[:]:  # 使用淺複製以便在迴圈中安全移除
        finished = ex.update()  # 更新動畫狀態，若回傳 True 則表示播放完畢
        ex.draw(screen)  # 繪製目前的爆炸幀
        if finished:
            explosions.remove(ex)  # 播放完畢後從清單移除，釋放記憶體

    # ------------------ 處理碰撞後的無敵與閃爍邏輯 ------------------
    if invulnerable:
        invuln_timer += 1  # 無敵計時器增加
        flash_counter += 1  # 用於控制閃爍頻率
        # 無敵時間結束，恢復可被攻擊
        if invuln_timer >= invuln_duration:
            invulnerable = False
            invuln_timer = 0
            flash_counter = 0

    # ------------------ 繪製玩家（支援閃爍效果） ------------------
    # 若遊戲尚未結束才繪製玩家與噴焰
    if not game_over:
        # 閃爍：在無敵期間每隔幾幀不畫出玩家達到閃爍效果
        if invulnerable:
            # 每 6 幀切換一次顯示/隱藏（每秒約 10 次閃爍）
            if (flash_counter // 6) % 2 == 0:
                # 繪製火焰與飛機（同之前的流程）
                burner_pos_x = (
                    fighter_rect.centerx - burner_img.get_width() // 2 + burner_offset_x
                )
                burner_pos_y = (
                    fighter_rect.bottom - burner_img.get_height() + burner_offset_y
                )
                screen.blit(burner_img, (burner_pos_x, burner_pos_y))
                screen.blit(fighter_img, fighter_rect)
        else:
            # 非無敵直接繪製（飛機與噴焰）
            burner_pos_x = (
                fighter_rect.centerx - burner_img.get_width() // 2 + burner_offset_x
            )
            burner_pos_y = (
                fighter_rect.bottom - burner_img.get_height() + burner_offset_y
            )
            screen.blit(burner_img, (burner_pos_x, burner_pos_y))
            screen.blit(fighter_img, fighter_rect)

    else:
        # 遊戲結束時繪製 gameover 畫面在畫面中央
        go_rect = gameover_img.get_rect()
        go_rect.centerx = bg_width // 2
        go_rect.centery = bg_height // 2
        screen.blit(gameover_img, go_rect)
        # 在 gameover 畫面下方顯示最終分數，使用英文格式 'Score: {score}'
        try:
            # 使用較大的字體顯示最終分數以便清楚可見（size 36）
            go_font = pygame.font.SysFont(None, 36)  # 新增：game over 分數字體
            # 使用英文顯示格式 Score: {score}，符合需求
            final_text = go_font.render(
                f"Score: {score}", True, (255, 255, 255)
            )  # 新增：渲染最終分數
            # 將文字置中並放在 gameover 圖片下方 10 像素處
            final_x = (
                bg_width // 2 - final_text.get_width() // 2
            )  # 新增：計算水平置中 x
            final_y = go_rect.bottom + 10  # 新增：計算 y 座標在圖片下方 10 像素
            # 把最終分數繪製到畫面上
            screen.blit(final_text, (final_x, final_y))  # 新增：繪製最終分數文字
        except Exception:
            # 若字型渲染發生問題則略過，仍保持 gameover 畫面可見
            pass

    # ------------------ 繪製血量條（顯示在畫面左上） ------------------
    # 背景條
    bar_x, bar_y = 20, 20  # 血量條位置
    bar_width, bar_height = 200, 20  # 血量條尺寸
    # 外框（灰色）
    pygame.draw.rect(
        screen, (100, 100, 100), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4)
    )
    # 依照血量比例繪製紅色血量
    hp_ratio = max(0, player_hp) / 100.0
    fill_width = int(bar_width * hp_ratio)
    pygame.draw.rect(screen, (200, 0, 0), (bar_x, bar_y, fill_width, bar_height))
    # 血量文字（數字顯示）
    try:
        font = pygame.font.SysFont(None, 20)
        hp_text = font.render(f"HP: {player_hp}", True, (255, 255, 255))
        screen.blit(hp_text, (bar_x, bar_y + bar_height + 4))
    except Exception:
        # 若字型渲染發生問題則略過（確保持續運行）
        pass

    # ------------------ 繪製分數（顯示在畫面右上，字體較大以便閱讀） ------------------
    try:
        # 建立一個較大的字體，用來顯示右上角的即時分數（size 36）
        score_font = pygame.font.SysFont(None, 36)  # 新增：更大字體方便閱讀
        # 使用較大字體渲染分數文字，顯示格式為 Score: {score}
        score_text = score_font.render(
            f"Score: {score}", True, (255, 255, 255)
        )  # 新增：渲染分數文字
        # 計算文字放置位置：畫面右上，距離右邊 20 像素、上方 20 像素
        score_pos_x = bg_width - score_text.get_width() - 20  # 新增：計算 x 座標
        score_pos_y = 20  # 新增：設定 y 座標為 20
        # 在畫面上繪製分數文字
        screen.blit(score_text, (score_pos_x, score_pos_y))  # 新增：將分數貼到畫面上
    except Exception:
        # 若字型渲染或繪製發生問題則略過，避免影響主迴圈執行
        pass

    # ----------------- 能量回復邏輯（每隔指定毫秒回復） -----------------
    # 使用 pygame.time.get_ticks() 以毫秒為單位追蹤時間，當超過回復間隔時增加能量
    current_time_ms = pygame.time.get_ticks()  # 取得目前時間（毫秒）
    # 若距離上次回復超過設定間隔，則回復能量並更新上次回復時間
    if current_time_ms - last_energy_regen_time >= energy_regen_interval_ms:
        # 計算回復後的能量值並限制在最大值內
        energy = min(energy_max, energy + energy_regen_amount)
        # 更新上次回復時間為現在（防止在同一幀內重覆回復）
        last_energy_regen_time = current_time_ms

    # ----------------- 血量回復邏輯（每隔指定毫秒回復） -----------------
    # 使用 pygame.time.get_ticks() 以毫秒為單位追蹤時間，當超過血量回復間隔時增加玩家血量
    # current_time_ms 已在上方取得，直接使用以避免重複呼叫
    # 當距離上次血量回復超過設定間隔且遊戲未結束時，回復血量
    if not game_over and (
        current_time_ms - last_health_regen_time >= health_regen_interval_ms
    ):
        # 增加血量（每次固定回復 health_regen_amount）並確保不超過最大值 100
        player_hp = min(100, player_hp + health_regen_amount)
        # 更新上次血量回復時間為現在（避免在同一幀內重覆回復）
        last_health_regen_time = current_time_ms

    # ------------------ 繪製能量條（顯示於血量條下方） ------------------
    # 能量條位置略微下移以避免與血量文字重疊
    energy_bar_x = bar_x
    energy_bar_y = bar_y + bar_height + 28
    energy_bar_width = 200
    energy_bar_height = 12
    # 能量外框（灰色）
    pygame.draw.rect(
        screen,
        (100, 100, 100),
        (
            energy_bar_x - 2,
            energy_bar_y - 2,
            energy_bar_width + 4,
            energy_bar_height + 4,
        ),
    )
    # 能量填滿部分（藍色代表能量）
    energy_ratio = max(0, energy) / float(energy_max)
    energy_fill_width = int(energy_bar_width * energy_ratio)
    pygame.draw.rect(
        screen,
        (50, 150, 255),
        (energy_bar_x, energy_bar_y, energy_fill_width, energy_bar_height),
    )
    # 能量文字顯示（例如 Energy: 8/10）
    try:
        energy_text = font.render(
            f"Energy: {energy}/{energy_max}", True, (255, 255, 255)
        )
        screen.blit(energy_text, (energy_bar_x, energy_bar_y + energy_bar_height + 2))
    except Exception:
        pass

    pygame.display.update()  # 更新畫面
