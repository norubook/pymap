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



'''
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# 背景ドット情報を2Dリストで用意（単純に0か1のマップ）
# 例えば40×30マス（20px四方のドット）
map_width, map_height = 40, 30
tile_size = 20

# 適当にランダムでドットを置く
import random
background_map = [[random.choice([0, 1]) for _ in range(map_width)] for _ in range(map_height)]

# カメラ座標（ピクセル単位）
camera_x = 0
camera_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_x -= 10
    if keys[pygame.K_RIGHT]:
        camera_x += 10
    if keys[pygame.K_UP]:
        camera_y -= 10
    if keys[pygame.K_DOWN]:
        camera_y += 10

    # 画面外にカメラが行かないように制限（マップ端まで）
    camera_x = max(0, min(camera_x, map_width * tile_size - screen.get_width()))
    camera_y = max(0, min(camera_y, map_height * tile_size - screen.get_height()))

    screen.fill((0, 0, 0))

    # 描画範囲のドットだけループ
    start_col = camera_x // tile_size
    end_col = (camera_x + screen.get_width()) // tile_size + 1
    start_row = camera_y // tile_size
    end_row = (camera_y + screen.get_height()) // tile_size + 1

    for row in range(start_row, end_row):
        for col in range(start_col, end_col):
            if 0 <= row < map_height and 0 <= col < map_width:
                if background_map[row][col] == 1:
                    # スクリーン座標に変換して描画
                    screen_x = col * tile_size - camera_x
                    screen_y = row * tile_size - camera_y
                    pygame.draw.rect(screen, (255, 255, 255), (screen_x, screen_y, tile_size, tile_size))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


このコード的にcsvを変換した後drowするんじゃなく配列に格納し描画する？
'''