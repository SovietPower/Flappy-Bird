# -*- coding: utf-8 -*-

'用来添加部分图片、音乐路径。一般只加载路径，不加载图片。'

import os, pygame
pygame.init()


FRAMERATE = 60
BIRD_X = 70
WIDTH, HEIGHT = 430, 600 # 实际活动区域。高度与地面的输出位置相同
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH, 760 # 屏幕大小

PATH = os.path.dirname(os.path.abspath(__file__))


# ! 事件定义
DIAMOND = pygame.event.custom_type()
ICE = pygame.event.custom_type()
UNFREEZE = pygame.event.custom_type()
UNFREEZE_PIPE = pygame.event.custom_type()

# ! 字体加载
# print(pygame.font.get_fonts())
my_font = pygame.font.SysFont('yaheiconsolashybrid',30) # 创建一个Font对象(系统自带)

# ! 音乐
background_music = os.path.join(PATH, 'music\\ZombiesOnYourLawn.ogg')
Diamond_music = os.path.join(PATH, 'music\\diamond.wav')
Ice_music = os.path.join(PATH, 'music\\ice_frozen.ogg')
Icemelon_music = os.path.join(PATH, 'music\\ice_melonimpact.ogg')

Hit_music = (
	os.path.join(PATH, 'music\\explode_cherrybomb.ogg'),
	os.path.join(PATH, 'music\\explode_explosion.ogg'),
	os.path.join(PATH, 'music\\explode_potato_mine.ogg')
)

Dave_music = (
	os.path.join(PATH, 'music\\crazydavecrazy.ogg'),
	os.path.join(PATH, 'music\\crazydaveextralong1.ogg'),
	os.path.join(PATH, 'music\\crazydaveextralong2.ogg'),
	os.path.join(PATH, 'music\\crazydaveextralong3.ogg'),
	os.path.join(PATH, 'music\\crazydavelong1.ogg'),
	os.path.join(PATH, 'music\\crazydavelong2.ogg'),
	os.path.join(PATH, 'music\\crazydavelong3.ogg'),
	os.path.join(PATH, 'music\\crazydavescream.ogg'),
	os.path.join(PATH, 'music\\crazydavescream2.ogg'),
	os.path.join(PATH, 'music\\crazydaveshort1.ogg'),
	os.path.join(PATH, 'music\\crazydaveshort2.ogg'),
	os.path.join(PATH, 'music\\crazydaveshort3.ogg')
)

# ! 图片
bird_up = pygame.image.load(os.path.join(PATH, 'pics\\bluebird_up_flap.png'))
bird_mid = pygame.image.load(os.path.join(PATH, 'pics\\bluebird_mid_flap.png'))
bird_down = pygame.image.load(os.path.join(PATH, 'pics\\bluebird_down_flap.png'))
bird_up_shield = pygame.image.load(os.path.join(PATH, 'pics\\bluebird_up_flap_shield.png'))
bird_mid_shield = pygame.image.load(os.path.join(PATH, 'pics\\bluebird_mid_flap_shield.png'))
bird_down_shield = pygame.image.load(os.path.join(PATH, 'pics\\bluebird_down_flap_shield.png'))
bird_void = pygame.image.load(os.path.join(PATH, 'pics\\bird_void.png'))

plant_food_image = pygame.image.load(os.path.join(PATH, 'pics\\plant_food.png'))

pipe_up = pygame.image.load(os.path.join(PATH, 'pics\\pipe_green_up.png'))
pipe_down = pygame.image.load(os.path.join(PATH, 'pics\\pipe_green_down.png'))

Diamond_image = os.path.join(PATH, 'pvz_pics\\Diamond.png')
Ice_image = os.path.join(PATH, 'pvz_pics\\Ice_WinterMelon_projectile.png')

Explode_image = (
	os.path.join(PATH, 'pvz_pics\\ExplosionCloud.png'),
	os.path.join(PATH, 'pvz_pics\\ExplosionPow.png'),
	os.path.join(PATH, 'pvz_pics\\ExplosionPowie.png'),
	os.path.join(PATH, 'pvz_pics\\Explosion_PotatoMine_mashed.png'),
	os.path.join(PATH, 'pvz_pics\\ExplosionSpudow.png')
)









