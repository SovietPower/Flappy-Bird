# -*- coding: utf-8 -*-

import os, sys, pygame, random
from random import randint
from threading import Timer
from itertools import cycle
pygame.init()

PATH = os.path.dirname(os.path.abspath(__file__))
PATH_FA = os.path.dirname(PATH)

# ! 导入父目录的cfg
sys.path.append(PATH_FA)
from cfg import *

# ! Sprite专有图片加载

# ! Sprite所需函数
def Dis_square(p1, p2):
	return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2

def Get_Pos(rect):
	'根据rect大小，返回地图中的随机合法位置'
	return (random.randint(0, WIDTH-rect.width), random.randint(0, HEIGHT-rect.height))

def Get_Pos_Bird(rect, p_bird):
	'根据rect大小，返回地图中的随机合法位置，但要与鸟有一定距离'
	p = 0
	while True:
		p = (random.randint(0, WIDTH-rect.width), random.randint(0, HEIGHT-rect.height))
		if Dis_square(p, p_bird)>40000: break
	return p

def Fix_Rect(rect):
	'保证Rect不越界'
	rect.left = min(max(0, rect.left), WIDTH-rect.width)
	rect.top = min(max(0, rect.top), HEIGHT-rect.height)

def rotate(image, rect, angle):
	"""Rotate the image while keeping its center."""
	# Rotate the original image without modifying it.
	# `rotozoom` usually looks nicer than `rotate`.
	new_image = pygame.transform.rotozoom(image, angle, 1)
	# Get a new rect with the center of the old rect.
	new_rect = new_image.get_rect(center=rect.center)
	Fix_Rect(new_rect)
	return new_image, new_rect

def Sprite_Rotate(self, time):
	self.total_time += time
	if self.total_time>=30:
		self.total_time = 0
		self.rotate_cnt = (self.rotate_cnt+1)%36
		self.print_image, self.rect = rotate(self.image, self.rect, 10*self.rotate_cnt) # 不要用同一物体旋转多次，而是调角度

# ! Sprite类
class Bird(pygame.sprite.Sprite):
	'''鸟！'''
	def __init__(self, position) -> None:
		pygame.sprite.Sprite.__init__(self)
		self.image = bird_down
		self.image_jump = bird_up
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = position
		self.jump = False
		self.jumpSpeed = 0.35
		self.gravity = 0.3
		self.dead = False
		self.time = 0
		self.jump_time = 0 # 已跳跃时间
		self.jump_duration = 150 # 单次跳跃时间
		self.speed_x = 0.5
		'无敌效果'
		self.shielded = False
		self.isSparking = False
		self.spark_cnt = 0
		self.spark_image = cycle([bird_down, bird_down_shield])
		self.spark_image_jump = cycle([bird_up, bird_up_shield])

	@property
	def x(self): return self.rect.left
	@property
	def y(self): return self.rect.top
	@x.setter
	def x(self, val): self.rect.left = val
	@y.setter
	def y(self, val): self.rect.top = val

	def update(self, time):
		'更新跳跃/降落后的状态'
		if self.jump:
			self.Jump(time)
			self.jump_time += time
			if self.jump_time>self.jump_duration:
				self.jump = False
				self.jump_time = 0
		else: self.Drop(time)

		self.time += time # 记录当前进行的时间，提高难度
		if self.time//5000!=0: # 每隔5s减少单次上升速度、提高降落速度
			self.time = 0
			# self.jumpSpeed = max(2, self.jumpSpeed-0.5)
			# self.gravity = min(10, self.gravity+0.4)
		if self.y<0: self.y=0
		if self.y+self.rect.height>HEIGHT:
			self.y = HEIGHT-self.rect.height
			if not self.shielded:
				self.dead = True # 注意判shielded。

		'闪烁效果'
		if self.isSparking:
			self.spark_cnt+=1
			if self.spark_cnt>3:
				self.spark_cnt=0
				self.image = next(self.spark_image)
				self.image_jump = next(self.spark_image_jump)

	def Jump(self, time):
		self.y -= self.jumpSpeed*time
	def Drop(self, time):
		self.y += self.gravity*time
	def MoveLeft(self, time):
		self.x = max(self.x-self.speed_x*time, 0)
	def MoveRight(self, time):
		self.x = min(self.x+self.speed_x*time, WIDTH-self.rect.width)

	def Shielded(self):
		self.shielded = True
		self.image = bird_down_shield
		self.image_jump = bird_up_shield
		Timer(2, self.ShieldSparking).start()
	def ShieldSparking(self):
		self.spark_cnt = 0
		self.isSparking = True
		Timer(2, self.finishShielded).start()
	def finishShielded(self):
		self.shielded = False
		self.isSparking = False
		self.image = bird_down
		self.image_jump = bird_up



class Pipe_Part(pygame.sprite.Sprite):
	'管子的上部或下部'
	def __init__(self, image, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = pos


class Pipe(pygame.sprite.Sprite):
	'管子的上部和下部'
	def __init__(self, image_up, image_down, speed):
		pygame.sprite.Sprite.__init__(self)
		self.speed = speed
		self.space = 170 # 管道间的距离，可能随时间而变
		self.x = WIDTH
		self.y = random.randint(20, HEIGHT-self.space-20) # 空隙开始位置
		self.width = image_up.get_width()
		self.height = image_up.get_height()
		self.y_up = self.y-self.height
		self.y_down = self.y+self.space

		self.up = Pipe_Part(image_up, (self.x, self.y_up))
		self.down = Pipe_Part(image_down, (self.x, self.y_down))

	def update(self, time, screen):
		self.x -= self.speed*time
		self.up.rect.left = self.x
		self.down.rect.left = self.x
		if self.x+self.width<0: return 0
		screen.blit(self.up.image, (self.x, self.y_up))
		screen.blit(self.down.image, (self.x, self.y_down))
		return 1



class Ball(pygame.sprite.Sprite):
	def __init__(self, image, speed):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = Get_Pos(self.rect)
		self.speed = speed
		self.speed0 = speed
		'Sprite Rotate'
		self.total_time, self.rotate_cnt = 0, 0
		self.print_image = self.image

	def update(self, time, screen):
		Sprite_Rotate(self, time)

		self.rect.move_ip(self.speed)
		screen.blit(self.print_image, self.rect)

		if self.rect.left<0 or self.rect.right>WIDTH:
			self.speed[0]*=-1
		if self.rect.top<0 or self.rect.bottom>HEIGHT:
			self.speed[1]*=-1


class PlantFood(pygame.sprite.Sprite):
	def __init__(self, image, speed, p_bird):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = Get_Pos_Bird(self.rect, p_bird)
		self.speed = speed

	def update(self, screen):
		self.rect.move_ip(self.speed)
		screen.blit(self.image, self.rect)

		if self.rect.left<0 or self.rect.right>WIDTH:
			self.speed[0]*=-1
		if self.rect.top<0 or self.rect.bottom>HEIGHT:
			self.speed[1]*=-1



class Diamond(pygame.sprite.Sprite):
	def __init__(self, image, p_bird):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = Get_Pos_Bird(self.rect, p_bird)
		self.time = 0 # 为每个Diamond设定计时器，比用event设定计时器更准确
		self.last = 3000 # 持续时间
		self.reward = 2000 # 奖励得分
	def update(self, time, screen):
		self.time += time
		'出现时间'
		if self.time>self.last: return 0
		screen.blit(self.image, self.rect)
		return 1


class Ice(pygame.sprite.Sprite):
	def __init__(self, image, p_bird):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = Get_Pos_Bird(self.rect, p_bird)
		self.time = 0
		self.last = 2500 # 持续时间
		self.freeze_time = 1200 # 冰冻时间
		self.freeze_rate = 2 # 减慢速率
		self.freeze_rate_pipe = 1.5 # 对水管减慢速率
		self.freeze_rate_time = 3500 # 减慢时间
		'Sprite Rotate'
		self.total_time, self.rotate_cnt = 0, 0
		self.print_image = self.image

	def update(self, time, screen):
		self.time += time
		'出现时间'
		if self.time>self.last: return 0
		Sprite_Rotate(self, time)
		screen.blit(self.print_image, self.rect)
		return 1

	def Freeze_Ball(self, balls):
		'解冻效果，可用set_timer'
		if random.randint(0, 2)==0:
			'完全冻结'
			for ball in balls:
				ball.speed = [0, 0]
			pygame.event.clear(eventtype=UNFREEZE)
			pygame.time.set_timer(UNFREEZE, self.freeze_time, True)
		else:
			'减速'
			for ball in balls:
				ball.speed = list(map(lambda x:x/self.freeze_rate, ball.speed))
			pygame.event.clear(eventtype=UNFREEZE)
			pygame.time.set_timer(UNFREEZE, self.freeze_rate_time, True)

	def Freeze_Pipe(self, pipes):
		'减速'
		for pipe in pipes:
			pipe.speed = pipe.speed/self.freeze_rate_pipe
		pygame.event.clear(eventtype=UNFREEZE_PIPE)
		pygame.time.set_timer(UNFREEZE_PIPE, self.freeze_rate_time, True)




















