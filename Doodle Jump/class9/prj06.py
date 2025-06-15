###################### 載入套件 ######################
import pygame
import sys
import random  # 匯入隨機模組


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
                        self.rect.bottom = platform.rect.top  # 主角底部對齊平台頂部
                        self.velocity_y = self.jump_power  # 彈跳
                        self.on_platform = True
                        return True
        self.on_platform = False
        return False


class Platform:
    def __init__(self, x, y, width, height, color):
        """
        初始化平台\n
        x, y: 平台左上角座標\n
        width, height: 平台寬高\n
        color: 平台顏色\n
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, display_area):
        """
        繪製平台\n
        display_area: 顯示畫布\n
        """
        pygame.draw.rect(display_area, self.color, self.rect)


###################### 定義函式區 ######################
# 畫面捲動與平台管理函式
# 依照步驟6，當主角上升到畫面中間以上時，畫面會捲動，平台自動生成與移除


def update_camera(
    player, platforms, win_height, win_width, platform_w, platform_h, platform_color
):
    """
    畫面捲動與平台自動生成/移除\n
    player: 主角物件\n
    platforms: 平台列表\n
    win_height, win_width: 視窗高寬\n
    platform_w, platform_h, platform_color: 平台尺寸與顏色\n
    """
    screen_middle = win_height // 2  # 畫面中間位置
    camera_move = 0
    # 若主角上升到畫面中間以上，固定主角在中間，平台往下移動
    if player.rect.y < screen_middle:
        camera_move = screen_middle - player.rect.y
        player.rect.y = screen_middle
        # 所有平台往下移動camera_move
        for platform in platforms:
            platform.rect.y += camera_move
    # 移除超出畫面底部的平台
    platforms[:] = [p for p in platforms if p.rect.top < win_height]
    # 追蹤最高平台的y座標
    y_min = min([p.rect.y for p in platforms]) if platforms else win_height
    # 平台數量不足時，自動在最高平台上方生成新平台
    while len(platforms) < 18:  # 預設平台數量(8~10+10)
        x = random.randint(0, win_width - platform_w)
        y = y_min - 60  # 新平台間距60像素
        new_platform = Platform(x, y, platform_w, platform_h, platform_color)
        platforms.append(new_platform)
        y_min = y


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

###################### 平台設定 ######################
# 平台寬度、高度、顏色
platform_w = 60
platform_h = 10
platform_color = (255, 255, 255)  # 白色

# 建立平台列表，並隨機產生8~10個平台
platforms = []  # 平台物件列表

# 先建立底部平台，確保玩家不會掉下去
platform_x = (win_width - platform_w) // 2
platform_y = win_height - platform_h - 10
base_platform = Platform(platform_x, platform_y, platform_w, platform_h, platform_color)
platforms.append(base_platform)

# 隨機產生其餘平台，數量為8~10個，y座標依序往上排列，間距60像素
platform_count = random.randint(8, 10)
for i in range(platform_count):
    x = random.randint(0, win_width - platform_w)
    y = (win_height - 100) - (i * 60)
    platform = Platform(x, y, platform_w, platform_h, platform_color)
    platforms.append(platform)

###################### 主程式 ######################
clock = pygame.time.Clock()
while True:
    clock.tick(60)  # 設定FPS為60
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 取得目前按下的按鍵狀態
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, win_width)  # 向左移動
    if keys[pygame.K_RIGHT]:
        player.move(1, win_width)  # 向右移動

    # 應用重力，讓主角自動下落
    player.apply_gravity()
    # 檢查主角是否落在任一平台上，並處理彈跳
    player.check_platform_collision(platforms)

    # 畫面捲動與平台自動生成/移除
    update_camera(
        player, platforms, win_height, win_width, platform_w, platform_h, platform_color
    )

    screen.fill((0, 0, 0))  # 填滿黑色背景
    player.draw(screen)  # 繪製主角
    # 繪製所有平台
    for platform in platforms:
        platform.draw(screen)
    pygame.display.update()  # 更新畫面
