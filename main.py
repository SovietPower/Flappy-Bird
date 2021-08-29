# -*- coding: utf-8 -*-

import os, sys, pygame, random
from random import randint

# from cfg import *
import cfg
from modules import *
from modules import Map # 用Map.x修改Map的全局变量

# ! Init
pygame.init()
pygame.display.set_caption("Flappy Bird")

screen = pygame.display.set_mode(cfg.SCREEN_SIZE)
PATH = os.path.dirname(os.path.abspath(__file__))

Speed = [[9, 12], [8, 5], [4, 9]] # list，可变的
Pipe_Speed_0 = 0.3
Pipe_Speed = Pipe_Speed_0

# ! 字体加载
# print(pygame.font.get_fonts())

# ! 图片加载
ball1_image = pygame.image.load(os.path.join(PATH, 'pics\\ball2.png'))
ball2_image = pygame.image.load(os.path.join(PATH, 'pics\\ball3.png'))
ball3_image = pygame.image.load(os.path.join(PATH, 'pics\\ball4.png'))
diamond1_image = pygame.image.load(cfg.Diamond_image)
ice_image = pygame.image.load(cfg.Ice_image)

# ! 音乐加载
Dave = tuple(map(pygame.mixer.Sound, cfg.Dave_music))
Dave_cnt = len(Dave)

hit = tuple(map(pygame.mixer.Sound, cfg.Hit_music))
for x in hit: x.set_volume(0.6)
hit_cnt = len(hit)

Diamond_get = pygame.mixer.Sound(cfg.Diamond_music)
# Diamond_get.set_volume(1) # 默认就是1(full volume)
Ice_get = pygame.mixer.Sound(cfg.Icemelon_music)
Ice_music = pygame.mixer.Sound(cfg.Ice_music)

# ! 一些全局的属性
clock = pygame.time.Clock()
Plant_Food_Timer = (3000, 7000, 12000, 18000, 25000, 33000, 41000, 51000, 61000, 73000, 85000, 100000, 110000, 125000, 140000) # 何时出现PlantFood


def Init():
	'声明并初始化全局变量'
	'global声明全局变量，会自动创建全局中未出现的全局变量'
	global bird, ball1, ball2, Start, Dead
	global Die_Time, Die_Type, Total_Time
	global ball_group, diamond_group, ice_group, pipe_group, food_cnt, food_group
	# 注意修改时要global，否则是新建了个局部变量！
	bird = Bird((BIRD_X, HEIGHT/2))
	Start, Dead = 0, 0
	Die_Time, Die_Type = 0, random.randint(0, Explode_cnt-1)
	Total_Time = 0
# ball
	ball_group = pygame.sprite.Group()
	ball_group.add(Ball(ball1_image, Speed[0]))
	ball_group.add(Ball(ball2_image, Speed[1]))
	ball_group.add(Ball(ball3_image, Speed[2]))
# background
	Map.map_x = MAP_DX
	Map.background_pos = [-MAP_DX, 0]
# diamond
	diamond_group = pygame.sprite.Group()
	# pygame.event.post(pygame.event.Event(DIAMOND)) # 用`pygame.event.Event(type, **attributes)`创建一个实例EventType后，再用`post`添加。
# ice
	ice_group = pygame.sprite.Group()
# pipe
	pipe_group = pygame.sprite.Group()
# plant food
	food_cnt = 0
	food_group = pygame.sprite.Group()
	# bird.Shielded() # 开局自带2s无敌

def Die(screen, bird):
	if bird.shielded: return
# 更新最高分
	global now_score, top_score
	top_score = now_score = Total_Time/1000
	old_file = os.path.join(PATH, 'player.txt')
	new_file = os.path.join(PATH, 'player_temp.txt')
	with open(old_file, 'r') as fin:
		with open(new_file, 'w') as fout:
			for line in fin:
				if line[0:19]=="Player's top score:":
					top_score = max(top_score, float(line[20:]))
					fout.write(f"Player's top score: {top_score:.2f}\n")
				else: fout.write(line)
	os.remove(old_file)
	os.rename(new_file, old_file)
# else
	global Dead, Die_Time, Die_Type
	Die_Time, Die_Type = 0, random.randint(0, Explode_cnt-1)
	Dead, bird.dead = 1, True
	hit[random.randint(0, hit_cnt-1)].play()
	DieMap(screen, bird, now_score, top_score, Die_Time, Die_Type)

def Disappear(group, time, screen):
	'道具消失，并返回消失数量'
	cnt = 0
	list = group.sprites()
	for x in list:
		if not x.update(time, screen):
			cnt+=1
			group.remove(x)
	return cnt

def Collide_Pipe(bird, pipe):
	return pygame.sprite.collide_rect(bird, pipe.up) or pygame.sprite.collide_rect(bird, pipe.down)


def main():
	global Start, Dead, bird, ball1, ball2, Pipe_Speed
	global Die_Time, Total_Time
	global food_cnt
# Init
	Init()

# music
	pygame.mixer.music.load(cfg.background_music)
	pygame.mixer.music.set_volume(1)
	pygame.mixer.music.play(-1)
	Dave_play_time = 0

# 计时器
	pygame.time.set_timer(DIAMOND, 2000, False)
	pygame.time.set_timer(ICE, 3000, False)

	while True:
		time = clock.tick(FRAMERATE) # 与上次循环间经过了多少毫秒
		time_s = time/1000
		Dave_play_time += time
		if Dead: Die_Time += time
		if Start and not Dead: Total_Time += time

		for ev in pygame.event.get():
			if ev.type == pygame.KEYDOWN:
				if Start and not Dead:
					if ev.key == pygame.K_UP:
						bird.jump = True
						bird.jump_time = 0
						if random.randint(1, 4)==1 and Dave_play_time>2000:
							Dave_play_time = 0
							Dave[random.randint(0, Dave_cnt-1)].play()
				if ev.key == pygame.K_r and Start: # Restart
					pipe = 0
					Init()
				elif ev.key == pygame.K_e: # enter
					if not Start: # 真正的开始游戏
						new = Pipe(pipe_up, pipe_down, Pipe_Speed)
						pipe_group.add(new)
						pygame.event.clear()
					Start = 1
			elif ev.type == pygame.QUIT:
				sys.exit()
			elif Start and not Dead:
				'道具'
				if ev.type == DIAMOND:
					new = Diamond(diamond1_image, (bird.x, bird.y))
					# new.update(0, screen) # 初始生成时绘制下避免被秒吃（实际太快了也看不出来）
					diamond_group.add(new)
				elif ev.type == ICE:
					new = Ice(ice_image, (bird.x, bird.y))
					ice_group.add(new)
				elif ev.type == UNFREEZE:
					'ball'
					for b in ball_group: b.speed = b.speed0
				elif ev.type == UNFREEZE_PIPE:
					'pipe'
					Pipe_Speed = Pipe_Speed_0
					for x in pipe_group: x.speed = Pipe_Speed

		if Start and not Dead:
			'move'
			press_key = pygame.key.get_pressed()
			if press_key[pygame.K_LEFT]:
				bird.MoveLeft(time)
			elif press_key[pygame.K_RIGHT]:
				bird.MoveRight(time)
			'plant food appears'
			if Total_Time>Plant_Food_Timer[food_cnt]+1000: # 能量豆难度调节
				food_cnt+=1
				if bool(food_group)==False:
					food_group.add(PlantFood(cfg.plant_food_image, [randint(3,8), randint(5,10)], (bird.x, bird.y)))

		if Start and not Dead:
			'游戏过程中的碰撞'
			'与水管碰撞'
			if pygame.sprite.spritecollide(bird, pipe_group, False, collided=Collide_Pipe):
				Die(screen, bird)
			'与球碰撞'
			# if pygame.sprite.spritecollide(bird, ball_group, False):
			# 	Die(screen, bird)
			'道具'
			if not Dead:
				'diamond'
				list = pygame.sprite.spritecollide(bird, diamond_group, True)
				for d in list:
					Diamond_get.play()
					Total_Time += d.reward
				'ice'
				list = pygame.sprite.spritecollide(bird, ice_group, True)
				for i in list:
					Ice_get.play()
					Ice_music.play()
					'ball'
					i.Freeze_Ball(ball_group.sprites())
					'pipe'
					Pipe_Speed/=i.freeze_rate_pipe
					i.Freeze_Pipe(pipe_group.sprites())
				'plant food'
				if not bird.shielded and pygame.sprite.spritecollide(bird, food_group, True)!=[]:
					bird.Shielded()

		if not Dead:
			if not Start:
				CreateMap_Intro(screen, bird, time_s) # 需要每帧都清空地图，再绘制其它物体，否则原先的物体不会被清除。
			else:
				bird.update(time)
				if not bird.dead:
					CreateMap(screen, bird, time_s, Total_Time)
				else: Die(screen, bird)
			'道具消失'
			Disappear(diamond_group, time, screen)
			Disappear(ice_group, time, screen)
		else:
			DieMap(screen, bird, now_score, top_score, Die_Time, Die_Type)

		ball_group.update(time, screen)
		food_group.update(screen)
		if Start and Disappear(pipe_group, time, screen):
			new = Pipe(pipe_up, pipe_down, Pipe_Speed)
			pipe_group.add(new)
		if Start:
			'游戏开始后才能覆盖所有（包括水管）'
			CreateGround(screen)



		pygame.display.update()











if __name__ == '__main__':
	main()


