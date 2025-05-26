##変数を用いて書き込みのon,offを行います.
##範囲外の座標を指定して読み取りを行う場合エラーが出るため，上下左右実装後座標を動かしてセーブする予定．
##予めサイズを決めておいた方がいい？
#全体マップ2000*2000
#フロアマップ1000*1000
#フロアマップか全体マップか把握するためにcsv1行目は特殊記号を用いるのが良いかも


import pygame
import sys
from pygame.locals import*
import json
import csv

SCREEN_SIZE = (500,500)

#保存とロード
#get_atではrgbと不透明度の形式で取得

def save_grid(filename,CELL_SIZE,screen):
    with open(filename, "w",newline="") as f: #newlineを外すと改行がおかしくなるため注意
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

def load_grid(filename,CELL_SIZE,screen):
    global grid
    try:
        with open(filename, "r",newline="") as f:
            reader = csv.reader(f)
            k=0
            for row in reader:
                for i in range(len(row)):
                    cell_col = row[i]
                    color_code =(0,0,0,0)
                    if cell_col =='w':
                        color_code =(255,255,255,255)
                    elif cell_col =='r':
                        color_code =(255,0,0,255)
                    elif cell_col =='g':
                        color_code =(0,255,0,255)
                    elif cell_col =='b':
                        color_code =(0,0,255,255)
                    else:
                        color_code =(255,255,255,255)
                    pygame.draw.rect(screen, color_code, (i*CELL_SIZE, k*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                k+=1

        print("読み込み完了。")
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
    input_active_save = False
    input_active_load = False
    input_text = ""
    font = pygame.font.Font(None, 36)
    #色

    WHITE = (255, 255, 255)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE  = (0, 0, 255)

    



    while True:

        print(f"\rsavemode ={input_active_save}             "
               f"loadmode ={input_active_load}            "
               f"input:{input_text}                        ",end = '',flush = True)
        
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
                if ((input_active_save == True) | (input_active_load == True)) & (event.key != pygame.K_RETURN):#ENTERキーはエラーを発生させるため入力から除外すること
                    if event.key== pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                if event.key == pygame.K_r:
                    current_color = RED
                elif event.key == pygame.K_g:
                    current_color = GREEN
                elif event.key == pygame.K_b:
                    current_color = BLUE
                elif event.key == pygame.K_w:
                    current_color = WHITE
                elif (event.key == pygame.K_s) & (input_active_save == False):
                    input_active_save = True
                    input_active_load = False
                    input_text = ""
                elif (event.key == pygame.K_RETURN) & (input_active_save == True):
                    input_active_save = False
                    save_grid(f"pymap/pymap/mapdata_{input_text}.csv",CELL_SIZE,screen)
                elif (event.key == pygame.K_l) & (input_active_load == False) :
                    input_active_load = True
                    input_active_save = False
                    input_text = ""
                elif (event.key == pygame.K_RETURN) & (input_active_load == True):
                    input_active_load = False
                    load_grid(f"pymap/pymap/mapdata_{input_text}.csv",CELL_SIZE,screen)

        pygame.display.flip()
            

if __name__== "__main__":
    main()