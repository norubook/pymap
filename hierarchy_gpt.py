import pygame
import sys

pygame.init()

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("可変ステージ遷移")

# 色
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
GREEN = (100, 255, 100)
BLACK = (0, 0, 0)

# 状態
STATE_MAP = "map"
STATE_STAGE = "stage"
current_state = STATE_MAP

# ステージ番号（どのステージにいるか）
current_stage = None

# ステージボタンの設定
stage_buttons = []
num_stages = 5
button_width = 200
button_height = 60
padding = 20

font = pygame.font.SysFont(None, 36)

for i in range(num_stages):
    x = 100 + (i % 3) * (button_width + padding)
    y = 100 + (i // 3) * (button_height + padding)
    rect = pygame.Rect(x, y, button_width, button_height)
    stage_buttons.append({"rect": rect, "stage_id": i})

clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_state == STATE_MAP:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in stage_buttons:
                    if button["rect"].collidepoint(event.pos):
                        current_stage = button["stage_id"]
                        current_state = STATE_STAGE

        elif current_state == STATE_STAGE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    current_state = STATE_MAP
                    current_stage = None

    # 表示切り替え
    if current_state == STATE_MAP:
        for button in stage_buttons:
            pygame.draw.rect(screen, BLUE, button["rect"])
            text = font.render(f"ステージ {button['stage_id']}", True, WHITE)
            screen.blit(text, (button["rect"].x + 20, button["rect"].y + 15))

    elif current_state == STATE_STAGE:
        text = font.render(f"ステージ {current_stage} をプレイ中！(qで戻る)", True, GREEN)
        screen.blit(text, (150, 250))

    pygame.display.flip()
    clock.tick(60)
