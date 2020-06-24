#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Software : PyCharm
# @File : onlyBird.py
# @Author : zhouzw
# @Created Time : 2020/6/24 10:04

import pygame
import sys

# 初始化pygame
pygame.init()
# 设置窗口
size = length, width = 320, 240
screen = pygame.display.set_mode(size)
# 载入图片
bird = pygame.image.load('assets/1.png')
# 获取坐标
bird_rect = bird.get_rect()
# 设置速度，背景颜色，时钟
speed = [5, 5]
color = (30, 40, 50)
clock = pygame.time.Clock()
while True:
    # 频率 tick时钟滴答
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # 直接exit()也可以，具体区别不详
    # 坐标随速度更新
    bird_rect = bird_rect.move(speed)
    # 碰撞边界检测  图片的rect.上下左右
    if bird_rect.left < 0 or bird_rect.right > length:
        speed[0] = -speed[0]
    if bird_rect.top < 0 or bird_rect.bottom > width:
        speed[1] = -speed[1]
    # 每次填充新背景，使图片逐帧显示
    screen.fill(color)
    # blit位块传输——实现动画效果
    screen.blit(bird, bird_rect)
    # flip翻页——重新绘制
    pygame.display.flip()
    # # update更新，和flip的区别没有深入学习
    # pygame.display.update(bird_rect)

