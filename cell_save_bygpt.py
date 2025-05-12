#下記プログラムはsample.pyに保存機能を追加してほしいとchatgptに入力したところ，
#出力されたプログラムです(出力結果より必要な箇所のみを引き出しています)．

import pygame
import sys
import json


#init系の書き方が参考にした方法と異なるため後で書き換えること

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("保存")

# 色定義
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

current_color = RED

# 初期グリッド（全マス白）
grid = [[WHITE for _ in range(COLS)] for _ in range(ROWS)]

def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(screen, grid[y][x],
                             (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # グリッド線
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y, WIDTH, y))

def save_grid(filename="dotdata.json"):
    with open(filename, "w") as f:
        # 色をRGBリストに変換して保存
        json.dump([[[r, g, b] for (r, g, b) in row] for row in grid], f)
    print("保存しました。")

def load_grid(filename="dotdata.json"):
    global grid
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            grid = [[tuple(cell) for cell in row] for row in data]
        print("読み込み完了。")
    except FileNotFoundError:
        print("保存ファイルが見つかりませんでした。")

# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid_x = x // CELL_SIZE
            grid_y = y // CELL_SIZE
            if 0 <= grid_x < COLS and 0 <= grid_y < ROWS:
                grid[grid_y][grid_x] = current_color

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                current_color = RED
            elif event.key == pygame.K_g:
                current_color = GREEN
            elif event.key == pygame.K_b:
                current_color = BLUE
            elif event.key == pygame.K_w:
                current_color = WHITE
            elif event.key == pygame.K_s:
                save_grid()
            elif event.key == pygame.K_l:
                load_grid()

    draw_grid()
    pygame.display.flip()


##    pygame.draw.line(screen, (200, 200, 200), (0, y, WIDTH, y))
## TypeError: function missing required argument 'end_pos' (pos 4)
## 実行時エラー発生しました．グリッド線を書いている部分に問題があるため，グリッド線を削除したsample.py
## に合わせて新しいプログラムを記述します．

'''
chatgptに聞くと
def save_minimal_indexed(filename="dotmap.json"):
    pixel_data = []
    for y in range(ROWS):
        for x in range(COLS):
            color = grid[y][x]
            if color != WHITE:
                hex_color = "#{:02X}{:02X}{:02X}".format(*color)
                pixel_data.append([x, y, hex_color])
    with open(filename, "w") as f:
        json.dump({"cell_size": CELL_SIZE, "pixels": pixel_data}, f)
    print("インデックス保存しました。")

def load_minimal_indexed(filename="dotmap.json"):
    global grid
    grid = [[WHITE for _ in range(COLS)] for _ in range(ROWS)]
    with open(filename, "r") as f:
        data = json.load(f)
        for px in data["pixels"]:
            x, y, hex_color = px
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            grid[y][x] = (r, g, b)
    print("インデックス読み込み完了。")

といった返答が来たけれど，今後ドットサイズの変換にも対応させるため
ドットあたり1つの場所で保存を行いたい．

ならfor文を
for y in range(ROWS/DOT_SIZE)
for x in range(COLS/DOT_SIZE)にして

color =grid[y*DOT_SIZE][x*DOT_SIZE]にする．
colorがwhiteかどうかは判定せず，そこにある色を読み取る．
簡易的にするためBLUEなら1，REDなら2のように数値で示す．
といった形で実装する考えです．

'''
