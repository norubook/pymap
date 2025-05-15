##現時点では参照するgridがないため対応策を考えます
##grid単位ではなくSCREEN_SIZEをCELL_SIZEで割って保存するサンプルの点を考える？
##読み込み時は保存されたサンプル点を元にドットに復元？

##変数を用いて書き込みのon,offも行いたい

import pygame
import sys
from pygame.locals import*
import json
import csv

SCREEN_SIZE = (500,500)

#保存とロード
#get_atではrgbと不透明度の形式で取得

def save_grid(filename,CELL_SIZE,screen):
    with open(filename, "w") as f:
        list =[]
        writer = csv.writer(f)
        for i in range(SCREEN_SIZE[1] // CELL_SIZE):
            for k in range(SCREEN_SIZE[0] // CELL_SIZE):
                cell_col = screen.get_at([k*CELL_SIZE,i*CELL_SIZE])
                if cell_col ==(255,255,255,255):
                    list.append('w')
                elif cell_col ==(255,0,0,255):
                    list.append('r')
                elif cell_col ==(0,255,0,255):
                    list.append('g')
                elif cell_col ==(0,0,255,255):
                    list.append('b')
                else:
                    list.append('n')
            writer.writerow(list)
            list=[]



    print("保存しました。")

def load_grid(filename):
    global grid
    try:
        with open(filename, "r") as f:
            data = f.read
            size = len(data[0]) 
        print("読み込み完了。")
        return f
    except FileNotFoundError:
        print("保存ファイルが見つかりませんでした。")

def main():

    #初期化
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("色記述サンプル")
    screen.fill((255,255,255))
    current_color = (255, 0, 0)
    CELL_SIZE = 20
    #色

    WHITE = (255, 255, 255)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE  = (0, 0, 255)

    



    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid_x = (x // CELL_SIZE) * CELL_SIZE
                grid_y = (y // CELL_SIZE) * CELL_SIZE
                pygame.draw.rect(screen, current_color, (grid_x, grid_y, CELL_SIZE, CELL_SIZE))

            # キーで色変更
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
                    save_grid("pymap/pymap/dotdata.csv",CELL_SIZE,screen)
                elif event.key == pygame.K_l:
                    file = load_grid("pymap/pymap/dotdata.csv")
                    

        pygame.display.flip()
            

if __name__== "__main__":
    main()