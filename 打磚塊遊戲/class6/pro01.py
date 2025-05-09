######################載入套件######################
import pygame
import sys
import random


######################物件類別######################
class Brick:
    def __init__(self, x, y, width, height, color, brick_type="normal"):
        """
        初始化磚塊\n
        x, y: 磚塊的左上角座標\n
        width, height: 磚塊的寬度和高度\n
        color: 磚塊的顏色\n
        brick_type: 磚塊類型 (normal, recover, bomb)
        """
        self.rect = pygame.Rect(x, y, width, height)  # 磚塊的矩形範圍
        self.color = color
        self.hit = False  # 磚塊是否被擊中
        self.brick_type = brick_type

    def draw(self, display_area):
        """
        繪製磚塊\n
        display: 顯示的畫布\n
        """
        if not self.hit:
            if self.brick_type == "recover":
                # 螢光外圈
                neon_color = (230, 232, 250, 40)
                neon_rect = pygame.Rect(
                    self.rect.x - 12,
                    self.rect.y - 12,
                    self.rect.width + 24,
                    self.rect.height + 24,
                )
                neon_surface = pygame.Surface(
                    (neon_rect.width, neon_rect.height), pygame.SRCALPHA
                )
                pygame.draw.rect(
                    neon_surface,
                    neon_color,
                    (0, 0, neon_rect.width, neon_rect.height),
                    border_radius=12,
                )
                display_area.blit(neon_surface, (neon_rect.x, neon_rect.y))
                # 亮金銀色光條
                glow_color = (230, 232, 250, 100)
                glow_rect = pygame.Rect(
                    self.rect.x - 4,
                    self.rect.y - 4,
                    self.rect.width + 8,
                    self.rect.height + 8,
                )
                glow_surface = pygame.Surface(
                    (glow_rect.width, glow_rect.height), pygame.SRCALPHA
                )
                pygame.draw.rect(
                    glow_surface,
                    glow_color,
                    (0, 0, glow_rect.width, glow_rect.height),
                    border_radius=6,
                )
                display_area.blit(glow_surface, (glow_rect.x, glow_rect.y))
            elif self.brick_type == "bomb":
                # 螢光外圈
                neon_color = (255, 0, 0, 40)
                neon_rect = pygame.Rect(
                    self.rect.x - 12,
                    self.rect.y - 12,
                    self.rect.width + 24,
                    self.rect.height + 24,
                )
                neon_surface = pygame.Surface(
                    (neon_rect.width, neon_rect.height), pygame.SRCALPHA
                )
                pygame.draw.rect(
                    neon_surface,
                    neon_color,
                    (0, 0, neon_rect.width, neon_rect.height),
                    border_radius=12,
                )
                display_area.blit(neon_surface, (neon_rect.x, neon_rect.y))
                # 暗紅色光條
                glow_color = (255, 0, 0, 100)
                glow_rect = pygame.Rect(
                    self.rect.x - 4,
                    self.rect.y - 4,
                    self.rect.width + 8,
                    self.rect.height + 8,
                )
                glow_surface = pygame.Surface(
                    (glow_rect.width, glow_rect.height), pygame.SRCALPHA
                )
                pygame.draw.rect(
                    glow_surface,
                    glow_color,
                    (0, 0, glow_rect.width, glow_rect.height),
                    border_radius=6,
                )
                display_area.blit(glow_surface, (glow_rect.x, glow_rect.y))
            pygame.draw.rect(display_area, self.color, self.rect)


class Ball:
    def __init__(self, x, y, radius, color):
        """
        初始化球\n
        x, y: 球的圓心座標\n
        radius: 球的半徑\n
        color: 球的顏色\n
        """
        self.x = x  # 球的x座標
        self.y = y  # 球的y座標
        self.radius = radius  # 球的半徑
        self.color = color  # 球的顏色
        self.speed_x = 5  # 球的x速度
        self.speed_y = -5  # 球的y速度
        self.is_moving = False  # 球是否在移動

    def draw(self, display_area):
        """
        繪製球\n
        display_area: 顯示的畫布\n
        """
        pygame.draw.circle(
            display_area, self.color, (int(self.x), int(self.y)), self.radius
        )

    def move(self):
        """
        移動球\n
        """
        if self.is_moving:
            self.x += self.speed_x  # 更新球的x座標
            self.y += self.speed_y  # 更新球的y座標

    def check_collision(self, bricks):
        """
        檢查碰撞並處理反彈\n
        bg_x, bg_y: 遊戲視窗寬高\n
        bricks: 磚塊列表\n
        pad: 底板物件
        """
        # 檢查與視窗邊緣的碰撞
        if self.x - self.radius < 0 or self.x + self.radius > bg_x:
            self.speed_x = -self.speed_x  # 水平反彈
        if self.y - self.radius <= 0:
            self.speed_y = -self.speed_y  # 垂直反彈

        if self.y + self.radius >= bg_y:
            self.is_moving = False

        if (
            self.y + self.radius >= pad.rect.y
            and self.y + self.radius <= pad.rect.y + pad.rect.height
            and self.x >= pad.rect.x
            and self.x <= pad.rect.x + pad.rect.width
        ):
            self.speed_y = -abs(self.speed_y)

        global score, lives, shake_until, can_control
        for brick in bricks:
            if not brick.hit:
                dx = abs(self.x - (brick.rect.x + brick.rect.width / 2))
                dy = abs(self.y - (brick.rect.y + brick.rect.height / 2))

                if dx <= (self.radius + brick.rect.width / 2) and dy <= (
                    self.radius + brick.rect.height / 2
                ):
                    brick.hit = True
                    # 撞到回復磚塊時生命+1
                    if brick.brick_type == "recover":
                        lives += 1
                    elif brick.brick_type == "bomb":
                        shake_until = pygame.time.get_ticks() + 3000
                        can_control = False
                    else:
                        score += 1
                    if (
                        self.x < brick.rect.x
                        or self.x > brick.rect.x + brick.rect.width
                    ):
                        self.speed_x = -self.speed_x
                    else:
                        self.speed_y = -self.speed_y


######################定義函式區######################
def reset_game():
    global bricks, ball, pad, score, lives, game_state, pause_until
    # 重設磚塊
    bricks.clear()
    total_bricks = bricks_row * bricks_column
    recover_count = random.randint(1, 10)
    bomb_count = random.randint(1, 15)
    recover_indices = random.sample(range(total_bricks), recover_count)
    bomb_indices = random.sample(
        [i for i in range(total_bricks) if i not in recover_indices], bomb_count
    )
    idx = 0
    for column in range(bricks_column):
        for row in range(bricks_row):
            x = column * (bricks_width + briaks_gap) + 70
            y = row * (bricks_height + briaks_gap) + 60
            if idx in recover_indices:
                color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                )  # 回復磚塊隨機顏色
                brick_type = "recover"
            elif idx in bomb_indices:
                color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                )  # 爆炸磚塊隨機顏色
                brick_type = "bomb"
            else:
                color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                )
                brick_type = "normal"
            brick = Brick(x, y, bricks_width, bricks_height, color, brick_type)
            bricks.append(brick)
            idx += 1
    # 重設底板
    pad.rect.x = 0
    pad.rect.y = bg_y - 48
    # 重設球
    ball.x = pad.rect.x + pad.rect.width // 2
    ball.y = pad.rect.y - ball_radius
    ball.speed_x = 5
    ball.speed_y = -5
    ball.is_moving = False
    # 重設分數與生命
    score = 0
    lives = 3
    game_state = "ready"
    pause_until = 0


######################初始化設定######################
pygame.init()  # 啟動pygame
FPS = pygame.time.Clock()  # 設定FPS
######################載入圖片######################

######################遊戲視窗設定######################
bg_x = 800
bg_y = 600  # 設定視窗大小
bg_size = (bg_x, bg_y)  # 設定視窗大小
pygame.display.set_caption("打磚塊遊戲")  # 設定視窗標題
screen = pygame.display.set_mode(bg_size)  # 建立視窗
######################磚塊######################
######################磚塊######################
bricks_row = 9  # 磚塊行數
bricks_column = 11  # 磚塊列數
bricks_width = 58  # 磚塊寬度
bricks_height = 16  # 磚塊高度
briaks_gap = 2  # 磚塊間距
bricks = []  # 磚塊列表(用來裝磚塊物件的列表)
import random  # 匯入隨機模組

total_bricks = bricks_row * bricks_column
recover_count = random.randint(1, 10)
bomb_count = random.randint(1, 15)
recover_indices = random.sample(range(total_bricks), recover_count)
bomb_indices = random.sample(
    [i for i in range(total_bricks) if i not in recover_indices], bomb_count
)
idx = 0
for column in range(bricks_column):  # 磚塊列數
    for row in range(bricks_row):  # 磚塊行數
        x = column * (bricks_width + briaks_gap) + 70  # 磚塊的x座標
        y = row * (bricks_height + briaks_gap) + 60  # 磚塊的y座標
        if idx in recover_indices:
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )  # 回復磚塊隨機顏色
            brick_type = "recover"
        elif idx in bomb_indices:
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )  # 爆炸磚塊隨機顏色
            brick_type = "bomb"
        else:
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )  # 隨機顏色
            brick_type = "normal"
        brick = Brick(x, y, bricks_width, bricks_height, color, brick_type)  # 磚塊物件
        bricks.append(brick)  # 將磚塊物件加入磚塊列表
        idx += 1
######################顯示文字設定######################
font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 32)
score = 0
lives = 3

game_state = "ready"  # ready, playing, gameover, win

######################底板設定######################
pad = Brick(
    0, bg_y - 48, bricks_width, bricks_height, (255, 255, 255)
)  # 初始化底板物件
######################球設定######################
ball_radius = 10  # 球的半徑
ball_color = (255, 215, 0)  # 金色
ball = Ball(
    pad.rect.x + pad.rect.width // 2, pad.rect.y - ball_radius, ball_radius, ball_color
)  # 初始化球物件

######################遊戲結束設定######################

######################新增fps#######################
FPS = pygame.time.Clock()  # 設定fps

# 初始化震動時間
shake_until = 0
# 新增控制權變數
can_control = True

######################主程式######################
while True:  # 無限迴圈
    FPS.tick(60)  # 設定fps為60
    # 處理震動效果
    now = pygame.time.get_ticks()
    if now < shake_until:
        shake_offset = (random.randint(-10, 10), random.randint(-10, 10))
        can_control = False
    else:
        shake_offset = (0, 0)
        can_control = True
    # 畫面填色時加上震動偏移
    screen.fill((0, 0, 0))
    mos_x, mos_y = pygame.mouse.get_pos()  # 取得滑鼠座標
    if now < shake_until:
        # 顯示震動訊息
        shake_surface = font.render(
            "你真弱，撞到爆炸磚塊。你這個小菜雞", True, (255, 0, 0)
        )
        screen.blit(
            shake_surface,
            (bg_x // 2 - 220 + shake_offset[0], bg_y // 2 - 20 + shake_offset[1]),
        )
    if game_state == "playing":
        if can_control:
            pad.rect.x = mos_x - pad.rect.width // 2  # 設定底板的x座標
            if pad.rect.x < 0:
                pad.rect.x = 0  # 如果底板的x座標小於0，則設定為0
            if pad.rect.x + pad.rect.width > bg_x:
                pad.rect.x = bg_x - pad.rect.width  # 限制底板的x座標不超過視窗的寬度
        if not ball.is_moving:
            ball.x = pad.rect.x + pad.rect.width // 2  # 設定球的x座標
            ball.y = pad.rect.y - ball_radius  # 設定球的y座標
        else:
            ball.move()
            ball.check_collision(bricks)
            # 檢查球是否掉落
            if not ball.is_moving:
                lives -= 1
                if lives <= 0:
                    game_state = "gameover"
                else:
                    # 球回到底板上
                    ball.x = pad.rect.x + pad.rect.width // 2
                    ball.y = pad.rect.y - ball_radius
            # 檢查是否全部磚塊都被擊中
            if all(brick.hit for brick in bricks):
                game_state = "win"
    else:
        # 遊戲未開始或結束時，球跟隨底板
        pad.rect.x = mos_x - pad.rect.width // 2
        if pad.rect.x < 0:
            pad.rect.x = 0
        if pad.rect.x + pad.rect.width > bg_x:
            pad.rect.x = bg_x - pad.rect.width
        ball.x = pad.rect.x + pad.rect.width // 2
        ball.y = pad.rect.y - ball_radius

    for event in pygame.event.get():  # 取得事件
        if event.type == pygame.QUIT:  # 如果事件是關閉視窗 (X)
            sys.exit()  # 結束程式
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "ready":
                ball.is_moving = True
                game_state = "playing"
            elif game_state in ("gameover", "win"):
                reset_game()
            elif (
                game_state == "playing"
                and not ball.is_moving
                and lives > 0
                and can_control
            ):
                ball.is_moving = True

    # 繪製磚塊、底板、球時加上震動偏移
    for brick in bricks:
        if not brick.hit:
            temp_rect = brick.rect.move(shake_offset)
            pygame.draw.rect(screen, brick.color, temp_rect)
    pad_rect = pad.rect.move(shake_offset)
    pygame.draw.rect(screen, pad.color, pad_rect)
    pygame.draw.circle(
        screen,
        ball.color,
        (int(ball.x + shake_offset[0]), int(ball.y + shake_offset[1])),
        ball.radius,
    )

    # 顯示分數在左上角
    score_surface = font.render(f"分數: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10 + shake_offset[0], 10 + shake_offset[1]))
    # 顯示剩餘生命在右上角
    lives_surface = font.render(f"生命: {lives}", True, (255, 255, 255))
    screen.blit(lives_surface, (bg_x - 150 + shake_offset[0], 10 + shake_offset[1]))

    # 顯示遊戲結束或勝利訊息
    if game_state == "gameover":
        over_surface = font.render("遊戲結束", True, (255, 0, 0))
        screen.blit(
            over_surface,
            (bg_x // 2 - 80 + shake_offset[0], bg_y // 2 - 40 + shake_offset[1]),
        )
        tip_surface = font.render("按滑鼠重新開始", True, (255, 255, 255))
        screen.blit(
            tip_surface,
            (bg_x // 2 - 120 + shake_offset[0], bg_y // 2 + 10 + shake_offset[1]),
        )
    elif game_state == "win":
        win_surface = font.render("你贏了，你真棒！👍", True, (0, 255, 0))
        screen.blit(
            win_surface,
            (bg_x // 2 - 120 + shake_offset[0], bg_y // 2 - 40 + shake_offset[1]),
        )
        tip_surface = font.render("按滑鼠重新開始", True, (255, 255, 255))
        screen.blit(
            tip_surface,
            (bg_x // 2 - 120 + shake_offset[0], bg_y // 2 + 10 + shake_offset[1]),
        )
    elif game_state == "ready":
        ready_surface = font.render("按滑鼠開始遊戲", True, (255, 255, 255))
        screen.blit(
            ready_surface,
            (bg_x // 2 - 120 + shake_offset[0], bg_y // 2 - 20 + shake_offset[1]),
        )

    pygame.display.update()  # 更新視窗
