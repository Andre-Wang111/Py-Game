###################### 載入套件 ######################
import pygame
import sys
import random  # 匯入隨機模組


###################### 彈簧生成機率設定 ######################
SPRING_PROBABILITY = 0.3  # 彈簧生成的機率(30%)


###################### 物件類別 ######################
class Player:
    def __init__(self, x, y, width, height, color):
        """
        初始化主角\n
        x, y: 主角左上角座標\n
        width, height: 主角寬高\n
        color: 主角顏色\n
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = 5  # 主角移動速度 (修正為5像素/次，依照說明)
        self.velocity_y = 0  # 垂直速度
        self.jump_power = -12  # 跳躍力量(負值向上)
        self.gravity = 0.5  # 重力加速度
        self.on_platform = False  # 是否站在平台上

    def draw(self, display_area):
        """
        繪製主角\n
        display_area: 顯示畫布\n
        """
        pygame.draw.rect(display_area, self.color, self.rect)

    def move(self, direction, bg_x):
        """
        控制主角左右移動，並實現穿牆效果\n
        direction: -1(左移) 或 1(右移)\n
        bg_x: 視窗寬度\n
        """
        self.rect.x += direction * self.speed  # 根據方向與速度移動
        # 穿牆效果：如果主角完全移出左邊界，從右側出現
        if self.rect.right < 0:
            self.rect.left = bg_x
        # 如果主角完全移出右邊界，從左側出現
        elif self.rect.left > bg_x:
            self.rect.right = 0

    def apply_gravity(self):
        """
        應用重力，讓主角自動下落\n
        """
        self.velocity_y += self.gravity  # 垂直速度增加重力
        self.rect.y += int(self.velocity_y)  # 更新主角y座標

    def check_platform_collision(self, platforms):
        """
        檢查主角是否落在任一平台上，並處理彈跳\n
        platforms: 平台物件列表\n
        """
        # 僅在主角往下掉時檢查碰撞
        if self.velocity_y > 0:
            # 根據下落速度，分段檢查每5像素，避免高速穿透平台
            steps = max(1, int(self.velocity_y // 5))
            for step in range(1, steps + 1):
                test_rect = self.rect.copy()
                test_rect.y += int(step * self.velocity_y / steps)
                for platform in platforms:
                    if (
                        test_rect.bottom <= platform.rect.top + abs(self.velocity_y)
                        and test_rect.bottom >= platform.rect.top
                        and test_rect.right > platform.rect.left
                        and test_rect.left < platform.rect.right
                    ):
                        if hasattr(platform, "is_breakable") and platform.is_breakable:
                            # 紅色平台：踩到後立即消失，並給予跳躍力
                            self.rect.bottom = platform.rect.top
                            self.velocity_y = self.jump_power
                            self.on_platform = True
                            platforms.remove(platform)
                            return True
                        else:
                            # 一般平台：主角底部對齊平台頂部並彈跳
                            self.rect.bottom = platform.rect.top  # 主角底部對齊平台頂部
                            self.velocity_y = self.jump_power  # 彈跳
                            self.on_platform = True
                            return True
        self.on_platform = False
        return False

    def check_spring_collision(self, springs):
        """
        檢查主角是否碰到任何彈簧，若碰撞則給予更高跳躍力
        springs: 彈簧物件列表
        """
        # 僅在主角往下掉時檢查碰撞
        if self.velocity_y > 0:
            # 根據下落速度，分段檢查每5像素，避免高速穿透彈簧
            steps = max(1, int(self.velocity_y // 5))
            for step in range(1, steps + 1):
                test_rect = self.rect.copy()
                test_rect.y += int(step * self.velocity_y / steps)
                for spring in springs:
                    # 檢查主角底部是否與彈簧頂部重疊，且左右有交集
                    if (
                        test_rect.bottom <= spring.rect.top + abs(self.velocity_y)
                        and test_rect.bottom >= spring.rect.top
                        and test_rect.right > spring.rect.left
                        and test_rect.left < spring.rect.right
                    ):
                        # 主角底部對齊彈簧頂部
                        self.rect.bottom = spring.rect.top
                        # 給予更高的跳躍力(往上跳25像素)
                        self.velocity_y = -25
                        self.on_platform = True
                        return True
        return False


class Platform:
    def __init__(self, x, y, width, height, color, is_breakable=False):
        """
        初始化平台\n
        x, y: 平台左上角座標\n
        width, height: 平台寬高\n
        color: 平台顏色\n
        is_breakable: 是否為只能踩一次的紅色平台 (預設False)\n
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_breakable = is_breakable  # 新增：是否為只能踩一次的平台

    def draw(self, display_area):
        """
        繪製平台\n
        display_area: 顯示畫布\n
        """
        pygame.draw.rect(display_area, self.color, self.rect)


###################### 新增彈簧(Spring)類別 ######################
class Spring:
    def __init__(self, x, y, width=20, height=10, color=(255, 255, 0)):
        """
        初始化彈簧道具
        x, y: 彈簧左上角座標 (通常在平台上方)
        width, height: 彈簧寬高 (預設20x10)
        color: 彈簧顏色 (預設黃色)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, display_area):
        """
        繪製彈簧道具
        display_area: 顯示畫布
        """
        pygame.draw.rect(display_area, self.color, self.rect)


###################### 定義函式區 ######################
# 畫面捲動與平台管理函式
# 依照步驟6，當主角上升到畫面中間以上時，畫面會捲動，平台自動生成與移除


def update_camera(
    player,
    platforms,
    springs,
    win_height,
    win_width,
    platform_w,
    platform_h,
    platform_color,
):
    """
    畫面捲動與平台/彈簧自動生成/移除 (平台與彈簧都會跟著畫面移動)
    player: 主角物件
    platforms: 平台列表
    springs: 彈簧列表
    win_height, win_width: 視窗高寬
    platform_w, platform_h, platform_color: 平台尺寸與顏色
    """
    screen_middle = win_height // 2  # 畫面中間位置
    camera_move = 0
    # 若主角上升到畫面中間以上，固定主角在中間，平台與彈簧往下移動
    if player.rect.y < screen_middle:
        camera_move = screen_middle - player.rect.y
        player.rect.y = screen_middle
        # 所有平台與彈簧往下移動camera_move
        for platform in platforms:
            platform.rect.y += camera_move
        for spring in springs:
            spring.rect.y += camera_move
    # 移除超出畫面底部的平台與彈簧
    platforms[:] = [p for p in platforms if p.rect.top < win_height]
    springs[:] = [s for s in springs if s.rect.top < win_height]
    # 追蹤最高平台的y座標
    y_min = min([p.rect.y for p in platforms]) if platforms else win_height
    # 平台數量不足時，自動在最高平台上方生成新平台
    while len(platforms) < 18:
        x = random.randint(0, win_width - platform_w)
        y = y_min - 60
        # 只有當 allow_breakable 為 True 時才有機率生成紅色平台
        is_breakable = False
        plat_color = platform_color
        if allow_breakable and random.random() < 0.2:
            is_breakable = True
            plat_color = (255, 0, 0)  # 紅色
        new_platform = Platform(x, y, platform_w, platform_h, plat_color, is_breakable)
        platforms.append(new_platform)
        # 以SPRING_PROBABILITY機率在新平台上方生成彈簧
        if random.random() < SPRING_PROBABILITY:
            spring_x = x + (platform_w - 20) // 2
            spring_y = y - 10
            spring = Spring(spring_x, spring_y)
            springs.append(spring)
        y_min = y


###################### 初始化設定 ######################
pygame.init()  # 啟動pygame

###################### 分數與遊戲結束相關變數 ######################
score = 0  # 當前分數
highest_score = 0  # 最高分數
initial_player_y = 0  # 玩家初始高度（稍後會設定）
font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 28)  # 使用微軟正黑體顯示分數
small_font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 20)
game_over = False  # 遊戲是否結束
allow_breakable = False  # 是否允許生成紅色平台（本局達到100分後才會變True）

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

###################### 平台設定 ######################
# 平台寬度、高度、顏色
platform_w = 60
platform_h = 10
platform_color = (255, 255, 255)  # 白色

# 建立平台列表，並隨機產生8~10個平台
platforms = []  # 平台物件列表
springs = []  # 彈簧物件列表 (新增)

# 先建立底部平台，確保玩家不會掉下去
platform_x = (win_width - platform_w) // 2
platform_y = win_height - platform_h - 10
base_platform = Platform(platform_x, platform_y, platform_w, platform_h, platform_color)
platforms.append(base_platform)
# 底部平台不產生彈簧

# 隨機產生其餘平台，數量為8~10個，y座標依序往上排列，間距60像素
platform_count = random.randint(8, 10)
for i in range(platform_count):
    x = random.randint(0, win_width - platform_w)
    y = (win_height - 100) - (i * 60)
    # 只有當 allow_breakable 為 True 時才有機率生成紅色平台
    is_breakable = False
    plat_color = platform_color
    if allow_breakable and random.random() < 0.2:
        is_breakable = True
        plat_color = (255, 0, 0)  # 紅色
    platform = Platform(x, y, platform_w, platform_h, plat_color, is_breakable)
    platforms.append(platform)
    # 以SPRING_PROBABILITY機率在平台上方生成彈簧，且不與平台重疊
    if random.random() < SPRING_PROBABILITY:
        spring_x = x + (platform_w - 20) // 2  # 彈簧水平置中
        spring_y = y - 10  # 彈簧在平台上方10像素
        spring = Spring(spring_x, spring_y)
        springs.append(spring)

###################### 主程式 ######################
clock = pygame.time.Clock()

while True:
    clock.tick(60)  # 設定FPS為60
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 遊戲結束時，按下任意鍵重新開始
        if game_over and event.type == pygame.KEYDOWN:
            # 重設主角位置與速度
            player.rect.x = win_width // 2 - player_width // 2
            player.rect.y = win_height - 50 - player_height
            player.velocity_y = 0
            # 先歸零分數，確保平台初始化時score為0
            score = 0
            initial_player_y = player.rect.y
            game_over = False
            allow_breakable = False  # 重生時必須重新達到100分才會出現紅色平台
            # 重新生成平台與彈簧
            platforms.clear()
            springs.clear()
            base_platform = Platform(
                platform_x, platform_y, platform_w, platform_h, platform_color
            )
            platforms.append(base_platform)
            platform_count = random.randint(8, 10)
            for i in range(platform_count):
                x = random.randint(0, win_width - platform_w)
                y = (win_height - 100) - (i * 60)
                # 只有當 allow_breakable 為 True 時才有機率生成紅色平台
                is_breakable = False
                plat_color = platform_color
                if allow_breakable and random.random() < 0.2:
                    is_breakable = True
                    plat_color = (255, 0, 0)  # 紅色
                platform = Platform(
                    x, y, platform_w, platform_h, plat_color, is_breakable
                )
                platforms.append(platform)
                # 以SPRING_PROBABILITY機率在平台上方生成彈簧
                if random.random() < SPRING_PROBABILITY:
                    spring_x = x + (platform_w - 20) // 2
                    spring_y = y - 10
                    spring = Spring(spring_x, spring_y)
                    springs.append(spring)
            # 分數歸零，重設初始高度
            score = 0
            initial_player_y = player.rect.y
            game_over = False
            allow_breakable = False  # 重生時必須重新達到100分才會出現紅色平台

    if not game_over:
        # 取得目前按下的按鍵狀態
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1, win_width)  # 向左移動
        if keys[pygame.K_RIGHT]:
            player.move(1, win_width)  # 向右移動

        # 應用重力，讓主角自動下落
        player.apply_gravity()
        # 先檢查主角是否碰到彈簧，若碰到則給予更高跳躍力
        # 若未碰到彈簧，才檢查平台碰撞
        if not player.check_spring_collision(springs):
            player.check_platform_collision(platforms)

        # 畫面捲動與平台自動生成/移除
        # 計算相機移動距離以計算分數
        screen_middle = win_height // 2
        camera_move = 0
        if player.rect.y < screen_middle:
            camera_move = screen_middle - player.rect.y
        # 呼叫整合後的update_camera (平台與彈簧一起處理)
        update_camera(
            player,
            platforms,
            springs,
            win_height,
            win_width,
            platform_w,
            platform_h,
            platform_color,
        )

        # 分數計算：每上升10像素加1分
        if camera_move > 0:
            score += int(camera_move / 10)
            if score > highest_score:
                highest_score = score
            # 達到100分後才允許生成紅色平台
            if not allow_breakable and score > 100:
                allow_breakable = True

        # 遊戲結束判斷：主角掉出畫面底部
        if player.rect.top > win_height:
            game_over = True

    # 畫面繪製
    screen.fill((0, 0, 0))  # 填滿黑色背景
    player.draw(screen)  # 繪製主角
    # 繪製所有平台
    for platform in platforms:
        platform.draw(screen)
    # 繪製所有彈簧 (新增)
    for spring in springs:
        spring.draw(screen)
    # 顯示分數與最高分
    score_text = font.render(f"分數: {score}", True, (255, 255, 0))
    high_text = small_font.render(f"最高分: {highest_score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(high_text, (10, 50))

    # 遊戲結束畫面
    if game_over:
        over_text = font.render("遊戲結束!", True, (255, 0, 0))
        restart_text = small_font.render("按任意鍵重新開始", True, (255, 255, 255))
        screen.blit(
            over_text,
            (win_width // 2 - over_text.get_width() // 2, win_height // 2 - 40),
        )
        screen.blit(
            restart_text,
            (win_width // 2 - restart_text.get_width() // 2, win_height // 2 + 10),
        )

    pygame.display.update()  # 更新畫面
