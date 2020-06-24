#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software : PyCharm
# @File : flappyBird.py
# @Author : zhouzw
# @Created Time : 2020/6/24 11:46


import pygame
import sys
import random


class Bird(object):
    """定义小鸟类"""

    def __init__(self):
        """初始化小鸟类"""
        # 状态
        self.birdRect = pygame.Rect(65, 50, 50, 50)
        # pygame.Rect()定义矩形，前两个参数为矩形左上角x、y值，后两个为宽、高
        self.liveStatus = True
        self.imageList = []
        for i in ['assets/0.png', 'assets/1.png', 'assets/2.png', 'assets/dead.png']:
            self.imageList.append(pygame.image.load(i))
        self.moveStatus = 0      # 运动状态
        self.jumpStatus = False  # 是否上跳

        # 参数  仅模拟，无物理意义！这里均初始化为0，具体值在最后的主程序中设置！
        self.jumpSpeed = 0  # 10
        self.fallSpeed = 0  # 5
        # 位置
        self.birdX = 120  # 仅确定位置，不更新
        self.birdY = 350  # 小鸟只有上下移动,无左右移动

    def updateBird(self):
        """更新小鸟运动状态"""
        # 每次按键都会触发更新，所以jumpSpeed和fallSpeed的初值必须在主程序中设置
        if self.jumpStatus:
            self.jumpSpeed -= 1         # 上跳速度迅速减慢
            self.birdY -= self.jumpSpeed
        else:
            self.fallSpeed += 0.2       # 下落速度渐渐增加
            self.birdY += self.fallSpeed

        self.birdRect[1] = self.birdY   # 更新小鸟矩形边界


class Pipline(object):
    """定义管道类"""

    def __init__(self):
        """初始化管道类"""
        self.pipX = 400  # 管道初位置
        self.top = pygame.image.load('assets/top.png')
        self.bottom = pygame.image.load('assets/bottom.png')

    def updatePipline(self):
        """更新管道状态"""
        step = 7             # 步长
        self.pipX -= step    # 从右向左移动，相对运动，模拟小鸟向右飞

        if self.pipX < -80:  # 出了左边界
            self.pipX = 400  # 重新从右边开始

            global score     # 设置全局变量
            score += 1       # 更新分数

            global topy,interval  # 随机化 上管道位置、上下间隔
            topy = random.random() * (-200) - 200  # (-400,200)
            interval = random.random() * 80 + 700  # (700, 780)
            # random.random()生成[0,1)范围内的一个实数


def creat_updateMap():
    """创建并更新地图：背景、小鸟、管道、分数"""
    # 显示背景
    background = pygame.image.load('assets/background.png')
    screen.blit(background, (0, 0))

    # 显示小鸟-设置小鸟生存、运动状态
    if not Bird.liveStatus:     # 死亡
        Bird.moveStatus = 3
    elif Bird.jumpStatus:       # 上跳
        Bird.moveStatus = 2
    elif not Bird.jumpStatus:   # 下落
        Bird.moveStatus = 1
    else:                       # 初始
        Bird.moveStatus = 0
    # 显示小鸟-显示不同状态对应的图片
    screen.blit(Bird.imageList[Bird.moveStatus], [Bird.birdX, Bird.birdY])
    # 更新小鸟状态
    Bird.updateBird()

    # 显示管道
    screen.blit(Pipline.top, [Pipline.pipX, topy])
    screen.blit(Pipline.bottom, [Pipline.pipX, topy + interval])
    # 更新管道状态
    Pipline.updatePipline()

    # 显示分数
    screen.blit(font.render('Score:' + str(score), 1, (255, 255, 255)), (100, 50))
    pygame.display.flip()  # 更新屏幕 update可以加参数更新局部，flip更新全局


def checkLive():
    """检测小鸟生死"""
    # 定义上下管道矩形
    topRect = pygame.Rect(Pipline.pipX, topy, Pipline.top.get_width(), Pipline.top.get_height())
    bottomRect = pygame.Rect(Pipline.pipX, topy + interval, Pipline.bottom.get_width(), Pipline.bottom.get_height())
    # 检测 管道、小鸟矩形碰撞
    if topRect.colliderect(Bird.birdRect) or bottomRect.colliderect(Bird.birdRect):
        Bird.liveStatus = False
        return 1  # 相撞而死
    # 检测 小鸟、边界碰撞
    if not 0 < Bird.birdRect[1] < height - 40:
        Bird.liveStatus = False
        return 1  # 越界而死
    else:
        return 0  # 正常飞翔


def printResult():
    """游戏结束，显示分数"""
    # 文本
    final_text0 = 'GAME OVER.'
    final_text1 = 'Final Score: ' + str(score)
    # 字体
    font0 = pygame.font.SysFont("Arial", 70)
    font1 = pygame.font.SysFont("Arial", 50)
    # 渲染
    ft0_surf = font0.render(final_text0, 1, (242, 3, 36))
    ft1_surf = font1.render(final_text1, 1, (253, 177, 36))
    # 显示
    screen.blit(ft0_surf, [30, 200])
    screen.blit(ft1_surf, [55, 300])


if __name__ == '__main__':
    """主函数"""
    pygame.init()  # 初始化

    size = width, height = 400, 650  # 使用 元组tuple 记录窗口size.
    # 任意无符号的对象，以逗号隔开，默认为元组
    screen = pygame.display.set_mode(size)  # 设置窗口 screen的type为<class 'pygame.Surface'>
    # color = (30, 40, 50)  # 背景颜色，此程序中未使用

    # 初始化字体类
    pygame.font.init()
    font = pygame.font.SysFont(None, 50)

    # 实例化 小鸟类、管道类、全局变量score
    Bird = Bird()
    Pipline = Pipline()
    score = 0
    # 初始化设置 top管道顶端对应y值，以及与bottom管道顶端间隔距离
    topy = -300
    interval = 750  # 间隔 上下管道顶端间隔距离

    clock = pygame.time.Clock()  # 时钟

    while 1:
        clock.tick(60)  # 更新频率
        # screen.fill(color)  # 设置背景为纯色，此程序未使用
        # print(Bird.jumpStatus)  # 测试用
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN and Bird.liveStatus:
                Bird.jumpStatus = True
                # 每次按键都是一次新的jump，下面两个参数必须每次都在这里设置声明
                Bird.jumpSpeed = 10
                Bird.fallSpeed = 5

        if Bird.jumpSpeed < 0:  # 下落时更新jumpStatus，对应图片也随之更新
            Bird.jumpStatus = False

        if checkLive():         # 死亡
            screen.blit(Bird.imageList[3], [Bird.birdX, Bird.birdY])  # 小鸟变灰色
            # pygame.display.update([Bird.birdX, Bird.birdY, 50, 50])
            pygame.display.flip()  # 更新屏幕 update可以加参数更新局部，flip更新全局
            printResult()  # 打印game over
        else:                   # 正常
            creat_updateMap()   # 主要步骤
