##変数を用いて書き込みのon,offを行います.
##範囲外の座標を指定して読み取りを行う場合エラーが出るため，上下左右実装後座標を動かしてセーブする予定．
##予めサイズを決めておいた方がいい？
#全体マップ2000*2000
#フロアマップ1000*1000
#フロアマップか全体マップか把握するためにcsv1行目は特殊記号を用いるのが良いかも


'''
現在状況

できたこと
移動した場合のロードやセーブをどうするか(仮置きで全体保存全体ロードとして実装)

任意の場所にロード

任意の場所にロードした場合，もしくは通常サイズより大きいマップをロードした場合，
　はみ出した部分だけ無視する方法

できていないこと

階層表示

関連マップをロードした場合，同じ場所を再ロードしないようにする方法．

'''


import pygame
import sys
from pygame.locals import*
import json
import csv

SCREEN_SIZE = [500,500]




#カラーコード
color_code={
    'w':(255,255,255,255),
    'r':(255,0,0,255),
    'g':(0,255,0,255),
    'b':(0,0,255,255),
}



#保存とロード
#get_atではrgb+不透明度の形式で取得

def save_grid(filename,CELL_SIZE,screen,name_data,wide,length,display_map):
    with open(filename, "w",newline="") as f: #newlineを外すと改行がおかしくなるため注意
        list =[]
        writer = csv.writer(f)
        #1行目データ
        list.append("ver2")
        list.append(name_data)
        list.append(wide)
        list.append(length)
        writer.writerow(list)
        list=[]
        for i in range(length//CELL_SIZE):
            list=(display_map[i])
            writer.writerow(list)



    print("保存しました。")


#ver2の場合のマップ情報の抽出関数
#想定返り値はname，wide，length


def load_ver2(map_info_row):
    #仮置き返り値
    map_info =[]
    connect_info ={}

    for i in map_info_row[:2]:
        map_info.append(i)
    for k in map_info_row[3:]:
        split_connect_info = k.split(':')
        key,values = split_connect_info[0],split_connect_info[1:]
        connect_info[key] = values


    return map_info,connect_info


#loadの関数

def load_grid(filename,display_map,start_point,max_CELL_num):
    global grid
    try:
        with open(filename, "r",newline="") as f:
            reader = csv.reader(f)
            k=start_point[1]
            #サイズ変更後の処理を設定後下記を適用してサイズを取得してください
            map_info_row=next(reader)
            if(map_info_row[0]=="ver2"):
                map_info,connect_info =load_ver2(map_info_row)
                
        
            for row in reader:
                for i in range(len(row)):
                    cell_col = row[i]
                    point_i=i+start_point[0]
                    if((point_i<max_CELL_num[0]) & (k<max_CELL_num[1])):
                        display_map[k][point_i]=cell_col
                    #描画位置拡張試し書き
                    #pygame.draw.rect(screen, color_code, ((i*CELL_SIZE)-current_coordinates, (k*CELL_SIZE)-current_coordinates, CELL_SIZE, CELL_SIZE))
                    #pygame.draw.rect(screen, color_code, ((i*CELL_SIZE), k*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                k+=1

        print("\r読み込み完了。             ",end = '',flush = True)
    except FileNotFoundError:
        print("\r保存ファイルが見つかりませんでした。               ",end = '',flush = True)

def load_hierarchy(hierarchy_csv):
    try:
        with open(hierarchy_csv, "r",newline="") as f:
            reader = csv.reader(f)
            #サイズ変更後の処理を設定後下記を適用してサイズを取得してください
            hierarchy_info_row=next(reader)
            map_info_row=next(reader)

        return int(hierarchy_info_row[2]),map_info_row
    except FileNotFoundError:
        return 0


def main():

    #初期化
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("pymap ver2.1")
    screen.fill((255,255,255))
    current_color = (255, 0, 0)
    CELL_SIZE = 20
    input_save_mode = False
    input_load_mode = False
    positiom_mode = False
    input_text = ""
    font = pygame.font.Font(None, 36)
    #色

    WHITE = (255, 255, 255)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE  = (0, 0, 255)

    #現在地
    
    current_coordinates=[0,0]




    #マップの設定
    max_CELL_num = [SCREEN_SIZE[0]//CELL_SIZE*2,SCREEN_SIZE[1]//CELL_SIZE*2]
    display_map = [['w' for a in range(max_CELL_num[0])]for b in range(max_CELL_num[1])]
    
    #直近のクリック位置保存(単位はドット)
    recent_click_cell = [0,0]


    #現在map表示しているのか階層表示しているのかを表す変数
    state_map = "map"
    state_hierarchy = "hierarchy"
    current_state = state_hierarchy

    #階層構造の初期設定
    hierarchy_buttons = []
    num_hierarchy = 1
    button_width = 200
    button_height = 60
    padding = 20

    #csvから階層構造データの読み取り
    num_hierarchy,map_name_datas =load_hierarchy("pymap/pymap/hierarchy_sample_v2.2.csv")

    #mapに記述する階層構造の情報の初期化
    hierarchy_mode = False
    stock_hierarchy = "None"



    while True:

        print(f"\rsavemode={input_save_mode}, loadmode={input_load_mode}, option={'p' if positiom_mode else '0-0'},  "
               f"hierarchy=:{stock_hierarchy},  input:{input_text}                                  ",end = '',flush = True)
        
        #階層構造表示用の仕組み仮置き場
        for i in range(num_hierarchy):
            hierarchy_button_x = 100 + (i % 3) * (button_width + padding)
            hierarchy_button_y = 100 + (i // 3) * (button_height + padding)
            rect = pygame.Rect(hierarchy_button_x, hierarchy_button_y, button_width, button_height)
            hierarchy_buttons.append({"rect": rect, "stage_id": i , "map_loc": f"pymap/pymap/mapdata_{map_name_datas[i]}.csv"})
        
        
        if (current_state == state_map):
            for k in range(max_CELL_num[1]):
                for i in range(max_CELL_num[0]):
                    cell_col = display_map[k][i]
                    '''
                    以下if文でコード振り分けする場合の文章
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
                    '''
                    color=color_code.get(cell_col,(255,255,255,255))
                    #描画位置拡張試し書き
                    pygame.draw.rect(screen, color, (((i-current_coordinates[0])*CELL_SIZE), ((k-current_coordinates[1])*CELL_SIZE), CELL_SIZE, CELL_SIZE))
                    #pygame.draw.rect(screen, color_code, ((i*CELL_SIZE), k*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        

        if (current_state == state_hierarchy):
            for button in hierarchy_buttons:
                pygame.draw.rect(screen, BLUE, button["rect"])
                text = font.render(f"hierarchy {button['stage_id']}F", True, WHITE)
                screen.blit(text, (button["rect"].x + 20, button["rect"].y + 15))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if current_state==state_map:
                    grid_x = (x // CELL_SIZE)+current_coordinates[0]
                    grid_y = (y // CELL_SIZE)+current_coordinates[1]
                    recent_click_cell = [grid_x,grid_y]
                    if current_color==RED:
                        display_map[grid_y][grid_x]='r' 
                    elif current_color==BLUE:
                        display_map[grid_y][grid_x]='b'   
                    elif current_color==WHITE:
                        display_map[grid_y][grid_x]='w'
                    elif current_color==GREEN:
                        display_map[grid_y][grid_x]='g' 
                    #pygame.draw.rect(screen, current_color, (grid_x*CELL_SIZE, grid_y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if current_state==state_hierarchy:
                    for button in hierarchy_buttons:
                        if button["rect"].collidepoint(event.pos):
                            load_grid(button["map_loc"],display_map,[0,0],max_CELL_num)
                            current_state = state_map


            # キーで色変更
            elif event.type == pygame.KEYDOWN:
                if ((input_save_mode) | (input_load_mode) |(hierarchy_mode)) & (event.key != pygame.K_RETURN):#ENTERキーはエラーを発生させるため入力から除外すること
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
                elif (event.key == pygame.K_1):
                    if (input_save_mode==False):
                        input_load_mode = False
                    input_save_mode= not(input_save_mode)
                    input_text = ""
                elif (event.key == pygame.K_RETURN) & (input_save_mode == True):
                    input_save_mode = False
                    save_grid(f"pymap/pymap/mapdata_v2_{input_text}.csv",CELL_SIZE,screen,input_text,1000,1000,display_map,stock_hierarchy)
                    stock_hierarchy = "None"
                elif (event.key == pygame.K_2):
                    if(input_load_mode==False):
                        input_save_mode = False
                        hierarchy_mode = False
                    input_load_mode= not(input_load_mode)
                    input_text = ""
                elif (event.key == pygame.K_3):
                    positiom_mode = not(positiom_mode)
                elif (event.key == pygame.K_RETURN) & (input_load_mode == True):
                    input_load_mode = False
                    if (positiom_mode):
                        load_grid(f"pymap/pymap/mapdata_v2_{input_text}.csv",display_map,recent_click_cell,max_CELL_num)
                    else:
                        load_grid(f"pymap/pymap/mapdata_v2_{input_text}.csv",display_map,[0,0],max_CELL_num)
                elif (event.key == pygame.K_4):
                    if(hierarchy_mode==False):
                        input_save_mode = False
                        input_load_mode = False
                    hierarchy_mode = not(hierarchy_mode)
                    input_text = ""
                elif (event.key == pygame.K_LEFT) & (current_coordinates[0]>0):
                    current_coordinates[0] -= 1
                elif (event.key == pygame.K_RIGHT) & (current_coordinates[0]<(max_CELL_num[0]-(SCREEN_SIZE[0]//CELL_SIZE))):
                    current_coordinates[0] += 1
                elif (event.key == pygame.K_UP) & (current_coordinates[1]>0):
                    current_coordinates[1] -= 1
                elif (event.key == pygame.K_DOWN) & (current_coordinates[1]<(max_CELL_num[1]-(SCREEN_SIZE[1]//CELL_SIZE))):
                    current_coordinates[1] += 1

        pygame.display.flip()
            

if __name__== "__main__":
    main()