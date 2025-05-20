#背景動作に必要な機能をGPTに聞いてみた



import pygame

pygame.init()

# 画面サイズ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 背景画像（大きめにするのがコツ）
background = pygame.image.load("background.jpg").convert()
bg_x = 0  # 背景のX座標

# プレイヤー画像（中央に描画するだけ）
player = pygame.Surface((50, 50))
player.fill((255, 0, 0))

running = True
speed = 5

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # キー入力で背景の位置を調整（逆方向に動かす）
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        bg_x += speed  # 背景を右に動かす → プレイヤーが左に動いてるように見える
    if keys[pygame.K_RIGHT]:
        bg_x -= speed  # 背景を左に動かす → プレイヤーが右に動いてるように見える

    # 背景とプレイヤーを描画
    screen.fill((0, 0, 0))  # 背景が足りないとき用に黒で塗りつぶす
    screen.blit(background, (bg_x, 0))  # 背景
    screen.blit(player, (WIDTH//2 - 25, HEIGHT//2 - 25))  # プレイヤー（固定）

    pygame.display.update()
    clock.tick(60)

pygame.quit()
