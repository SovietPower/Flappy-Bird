# -*- coding: utf-8 -*-

'绘制地图'

import os, sys, pygame, random
pygame.init()

PATH = os.path.dirname(os.path.abspath(__file__))
PATH_FA = os.path.dirname(PATH)

# ! 导入父目录的cfg
sys.path.append(PATH_FA)
from cfg import *


# ! 字体加载
# print(pygame.font.get_fonts())

# ! 图片加载
ground = pygame.image.load(os.path.join(PATH, 'pics\\base.png'))
welcome = pygame.image.load(os.path.join(PATH, 'pics\\welcome.png'))
game_over = pygame.image.load(os.path.join(PATH, 'pics\\game_over.png'))
# background = pygame.image.load(os.path.join(PATH, 'pics\\background_night.png'))
background = pygame.image.load(os.path.join(PATH, 'pics\\background_pvz2.png'))
bird_dead = pygame.image.load(os.path.join(PATH, 'pics\\dead.png'))

Explode = []
for x in Explode_image: Explode.append(pygame.image.load(x))
Explode_cnt = len(Explode)

# ! 音乐加载

# ! 某些常量
MAP_DX = 200
MAP_WIDTH = background.get_width()-100

# ! 某些变量
'speed为常量'
ground_x, ground_speed = 0, 100
wing_sum, wing_speed = 0, 300

map_x, map_speed = MAP_DX, 200 # 若不乘time，则speed除50或更多
background_pos = [-MAP_DX, 0]


def MoveMap(time):
	'没必要乘time(s)'
	global map_x, map_speed
	map_x += map_speed*time
	if map_x+WIDTH>MAP_WIDTH:
		map_x = MAP_WIDTH-WIDTH
		map_speed*=-1
	if map_x<MAP_DX:
		map_x = MAP_DX
		map_speed*=-1
	background_pos[0] = -map_x

def MoveGround(time):
	MoveMap(time) # 地面移动时，即游戏进行时，来移动背景
	global ground_x
	ground_x -= ground_speed*time
	if ground_x<-36: ground_x=max(-30, ground_x+36) # 限制x最小为-30，避免时间变化过大的情况

def MoveWing(time):
	'设置鸟扇动翅膀的效果，并返回当前翅膀状态图片'
	global wing_sum
	wing_sum += wing_speed*time
	if wing_sum>150: wing_sum%=150 # %=150 not -=150，避免时间变化过大的情况
	if 0<=wing_sum<=50: return bird_mid
	elif wing_sum<=100: return bird_up
	elif wing_sum<=150: return bird_down
	assert wing_sum>=0 and wing_sum<=150

def CreateGround(screen):
	'管道输出之后要单独输出地面'
	screen.blit(ground, (ground_x, 600)) # 地面高168

def CreateMap_Intro(screen, bird, time):
	'正式开始前的界面。鸟的动作是确定、不可操作的。'
	MoveGround(time) # 设置地面移动效果
	bird_image = MoveWing(time) # 设置鸟扇动翅膀的效果
# 地图
	screen.fill((255, 255, 255))
	screen.blit(background, background_pos) # 430*760
	screen.blit(ground, (ground_x, 600)) # 地面高168
	screen.blit(welcome, (77, 180)) # 276*400 x:430/2-276/2=215-138=77 y:760/2-400/2=180
	screen.blit(bird_image, (bird.x, bird.y))
# 提示
	color = (30, 30, 30)
	tip = my_font.render('操作说明：', True, color)
	tip1 = my_font.render('按E开始', True, color)
	tip2 = my_font.render('按Up/Left/Right使小鸟飞', True, color)
	tip3 = my_font.render('按R重新游戏 Wabby Wabbo', True, color)
	# screen.blit(tip, ((WIDTH-tip.get_width())/2, 560))
	screen.blit(tip, (20, 560))
	screen.blit(tip1, (20, 600))
	screen.blit(tip2, (20, 640))
	screen.blit(tip3, (20, 680))
	# pygame.display.update() # 此时没必要update，否则可能出现无绘制物体的瞬间画面

def CreateMap(screen, bird, time, Total_Time):
	'正式开始后的界面。鸟的动作要根据具体情况设定。'
	MoveGround(time)

	screen.fill((255, 255, 255))
	screen.blit(background, background_pos) # 430*760
	screen.blit(ground, (ground_x, 600)) # 地面高168
	if bird.jump: screen.blit(bird.image_jump, (bird.x, bird.y))
	else: screen.blit(bird.image, (bird.x, bird.y))

	now = my_font.render(f'当前得分：{Total_Time/1000:.2f}秒', True, (0, 0, 0))
	screen.blit(now, ((WIDTH-now.get_width())-20, (HEIGHT-now.get_height())-20))

def DieMap(screen, bird, now_score, top_score, Die_Time, Die_Type):
	'该函数不对Die_Time, Die_Type进行修改，两个变量保存在main中，由main修改'
	screen.fill((255, 255, 255))
	screen.blit(background, background_pos) # 430*760
	screen.blit(ground, (ground_x, 600)) # 地面高168
	screen.blit(bird_dead, (bird.x, bird.y))
	screen.blit(game_over, (61, 290)) # 308*68  x:(430-308)/2 y:(760-180)/2

	now = my_font.render(f'你的得分为：{now_score:.2f}秒！', True, (0, 0, 0))
	top = my_font.render(f'你的最高分为：{top_score:.2f}秒！', True, (0, 0, 0))
	screen.blit(now, ((WIDTH-now.get_width())/2, 430))
	screen.blit(top, ((WIDTH-top.get_width())/2, 460))

	# global Die_Time, Die_Type
	if Die_Time<1500:
		surf = Explode[Die_Type]
		screen.blit(surf, (bird.x-surf.get_width()/3, bird.y-surf.get_height()/2))




