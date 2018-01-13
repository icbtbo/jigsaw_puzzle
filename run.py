# -*- coding: utf-8 -*-
# @Date    : 2018-01-1 13:24:09
# @Author  : Icbtno
# @Link    : https://icbtbo.github.io

from tkinter import *
import pygame, sys, random, os, datetime, time
from pygame.locals import *
from PIL import Image, ImageTk
import shutil

# 图片列表
picts = ['pic1.png', 'pic2.jpg']

# 所选定的默认图片索引
p_number = 0

# 默认拼图格数
VHNUMS = 3

# 一些常量
WINDOWWIDTH = 500
WINDOWHEIGHT = 500
BACKGROUNDCOLOR = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FPS = 40
CELLNUMS = VHNUMS * VHNUMS
MAXRANDTIME = 100

# 退出
def terminate():
    pygame.quit()
    # sys.exit()


# 随机生成游戏盘面
def newGameBoard():
    board = []
    for i in range(CELLNUMS):
        board.append(i)
    blackCell = CELLNUMS - 1
    board[blackCell] = -1

    for i in range(MAXRANDTIME):
        direction = random.randint(0, 3)
        if (direction == 0):
            blackCell = moveLeft(board, blackCell)
        elif (direction == 1):
            blackCell = moveRight(board, blackCell)
        elif (direction == 2):
            blackCell = moveUp(board, blackCell)
        elif (direction == 3):
            blackCell = moveDown(board, blackCell)
    return board, blackCell


# 若空白图像块不在最左边，则将空白块左边的块移动到空白块位置
def moveRight(board, blackCell):
    if blackCell % VHNUMS == 0:
        return blackCell
    board[blackCell - 1], board[blackCell] = board[blackCell], board[blackCell - 1]
    return blackCell - 1


# 若空白图像块不在最右边，则将空白块右边的块移动到空白块位置
def moveLeft(board, blackCell):
    if blackCell % VHNUMS == VHNUMS - 1:
        return blackCell
    board[blackCell + 1], board[blackCell] = board[blackCell], board[blackCell + 1]
    return blackCell + 1


# 若空白图像块不在最上边，则将空白块上边的块移动到空白块位置
def moveDown(board, blackCell):
    if blackCell < VHNUMS:
        return blackCell
    board[blackCell - VHNUMS], board[blackCell] = board[blackCell], board[blackCell - VHNUMS]
    return blackCell - VHNUMS


# 若空白图像块不在最下边，则将空白块下边的块移动到空白块位置
def moveUp(board, blackCell):
    if blackCell >= CELLNUMS - VHNUMS:
        return blackCell
    board[blackCell + VHNUMS], board[blackCell] = board[blackCell], board[blackCell + VHNUMS]
    return blackCell + VHNUMS


# 是否完成
def isFinished(board, blackCell):
    for i in range(CELLNUMS - 1):
        if board[i] != i:
            return False
    return True

def draw_info(windowSurface, start_time, my_font, color, pos, finsh):
    if finsh:
        text_fmt = my_font.render('你太棒了！', 1, color)
        windowSurface.blit(text_fmt, pos)
        return True
    # 倒计时
    passtime = (datetime.datetime.now() - start_time).seconds
    text = '时间限制为 300 s， 您已花费' + str(passtime) + 's'
    if passtime > 300:
        text_fmt = my_font.render('超时，游戏结束！', 1, color)
        windowSurface.blit(text_fmt, pos)
        return False
    # 设置文字内容
    text_fmt = my_font.render(text, 1, color)
    # 绘制文字
    windowSurface.blit(text_fmt, pos)
    return True
# ====================================================================================================================

# 开始游戏 函数
def begin_game():
    # 初始化
    pygame.init()
    mainClock = pygame.time.Clock()
    starttime = datetime.datetime.now()

    # 加载图片
    gameImage = pygame.image.load(os.getcwd() + '\\' + 'pictures' + '\\' + picts[p_number])
    gameRect = gameImage.get_rect()

    # 创建字体对象
    my_font = pygame.font.SysFont('SimHei', 16)
    color = BLUE
    pos = (gameRect.width + 50, gameRect.height / 2)

    # 设置窗口
    windowSurface = pygame.display.set_mode((gameRect.width + 300, gameRect.height))
    pygame.display.set_caption('拼图')

    # 时间限制
    totaltime = 10

    cellWidth = int(gameRect.width / VHNUMS)
    cellHeight = int(gameRect.height / VHNUMS)

    finish = False
    running = True

    gameBoard, blackCell = newGameBoard()

    # 游戏主循环
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
                running = False
            if finish:
                continue
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    blackCell = moveLeft(gameBoard, blackCell)
                if event.key == K_RIGHT or event.key == ord('d'):
                    blackCell = moveRight(gameBoard, blackCell)
                if event.key == K_UP or event.key == ord('w'):
                    blackCell = moveUp(gameBoard, blackCell)
                if event.key == K_DOWN or event.key == ord('s'):
                    blackCell = moveDown(gameBoard, blackCell)
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                col = int(x / cellWidth)
                row = int(y / cellHeight)
                index = col + row * VHNUMS
                if (
                                        index == blackCell - 1 or index == blackCell + 1 or index == blackCell - VHNUMS or index == blackCell + VHNUMS):
                    gameBoard[blackCell], gameBoard[index] = gameBoard[index], gameBoard[blackCell]
                    blackCell = index

        if (isFinished(gameBoard, blackCell)):
            gameBoard[blackCell] = CELLNUMS - 1
            finish = True

        if running:
            windowSurface.fill(BACKGROUNDCOLOR)
            for i in range(CELLNUMS):
                rowDst = int(i / VHNUMS)
                colDst = int(i % VHNUMS)
                rectDst = pygame.Rect(colDst * cellWidth, rowDst * cellHeight, cellWidth, cellHeight)

                if gameBoard[i] == -1:
                    continue

                rowArea = int(gameBoard[i] / VHNUMS)
                colArea = int(gameBoard[i] % VHNUMS)
                rectArea = pygame.Rect(colArea * cellWidth, rowArea * cellHeight, cellWidth, cellHeight)
                windowSurface.blit(gameImage, rectDst, rectArea)

            for i in range(VHNUMS + 1):
                pygame.draw.line(windowSurface, BLACK, (i * cellWidth, 0), (i * cellWidth, gameRect.height))
            for i in range(VHNUMS + 1):
                pygame.draw.line(windowSurface, BLACK, (0, i * cellHeight), (gameRect.width, i * cellHeight))




            if not draw_info(windowSurface, starttime, my_font, BLUE, pos, finish):
                pygame.display.update()
                mainClock.tick(FPS)
                time.sleep(5)
                terminate()
                running = False
            if running:
                pygame.display.update()
                mainClock.tick(FPS)


# 查看原图 函数
def view_origin_pic():
    top = Toplevel()
    bm = ImageTk.PhotoImage(file=os.getcwd() + '\\' + 'pictures' + '\\' + picts[p_number])
    label = Label(top, image=bm)
    label.pack()
    top.mainloop()

# 切换图片 函数
def switch_pic():
    global p_number
    if p_number < len(picts):
        p_number = p_number + 1
    else:
        p_number = 0

# 切换难度
## 修改格数
def execute(e):
    global VHNUMS, CELLNUMS
    VHNUMS = int(e.get().strip())
    CELLNUMS = VHNUMS * VHNUMS

def revise_vhnum():
    tl = Toplevel()
    tl.title("修改拼图格数")
    tl.geometry('400x300')

    Label(tl, text='拼图格数').grid(row=0, sticky=W)
    e = Entry(tl)
    e.grid(row=0, column=1)

    button = Button(tl, text="修改", pady=6, command=lambda: execute(e))
    button.grid(row=5, column=1, sticky=W + E + N + S)

## 简单模式
def easy():
    global VHNUMS, CELLNUMS
    VHNUMS = 3
    CELLNUMS = VHNUMS * VHNUMS

## 普通模式
def normal():
    global VHNUMS, CELLNUMS
    VHNUMS = 4
    CELLNUMS = VHNUMS * VHNUMS

## 困难模式
def difficult():
    global VHNUMS, CELLNUMS
    VHNUMS = 5
    CELLNUMS = VHNUMS * VHNUMS

## 切换难度模块 主界面
def switch_difficulty():
    tl = Toplevel()
    tl.title("切换难度")
    tl.geometry('400x300')

    button1 = Button(tl, text="简单", padx=20, pady=16, command=easy)
    button1.place(relx=0.3, rely=0.3, anchor=CENTER)
    button2 = Button(tl, text="普通", padx=20, pady=16, command=normal)
    button2.place(relx=0.6, rely=0.3, anchor=CENTER)
    button3 = Button(tl, text="困难", padx=20, pady=16, command=difficult)
    button3.place(relx=0.3, rely=0.6, anchor=CENTER)
    button4 = Button(tl, text="自定义", padx=20, pady=16, command=revise_vhnum)
    button4.place(relx=0.6, rely=0.6, anchor=CENTER)

# 添加本地图片
def add_pict():
    path = os.getcwd()
    new_path = os.getcwd() + '\\' + 'pictures'

    for root, dirs, files in os.walk(path):
        for i in range(len(files)):
            if files[i][-3:] == 'jpg' or files[i][-3:] == 'png':
                file_path = root + '/' + files[i]
                new_file_path = new_path + '/' + files[i]
                shutil.move(file_path, new_file_path)
                global picts, p_number
                picts.append(files[i])
                p_number = len(picts) - 1
        break
# =====================================================================================================================

# 主函数
def main():
    root = Tk()
    root.title('拼图游戏')
    root.resizable(0, 0)
    root.geometry('400x300')

    button1 = Button(root, text="开始游戏", padx=20, pady=16, command=begin_game)
    button1.place(relx=0.25, rely=0.2, anchor=CENTER)
    button2 = Button(root, text="查看原图", padx=20, pady=16, command=view_origin_pic)
    button2.place(relx=0.75, rely=0.2, anchor=CENTER)
    button3 = Button(root, text="切换图片", padx=20, pady=16, command=switch_pic)
    button3.place(relx=0.25, rely=0.7, anchor=CENTER)
    button4 = Button(root, text="切换难度", padx=20, pady=16, command=switch_difficulty)
    button4.place(relx=0.75, rely=0.7, anchor=CENTER)
    button5 = Button(root, text="添加本地图片", padx=20, pady=16, command=add_pict)
    button5.place(relx=0.5, rely=0.45, anchor=CENTER)

    root.mainloop()

if __name__ == '__main__':
    main()