基于Flappy Bird的玩法做的小游戏，用来练习自己的Python。

## 前言
因为pvz的素材比较好获取，以及比较熟悉pvz，所以很多素材来自pvz解包。不过可能有点违和感。

只是学Python半个月左右后设计的，代码实现、文件结构可能不是很好（在改了），如有建议还请指出。

因为原游戏Flappy Bird的游戏性限制，该游戏的可玩性可能也不太高。

主要参考：[Pygame官方文档](https://www.pygame.org/docs/)

地面、翅膀的运动效果参考：[拇指笔记](https://blog.csdn.net/weixin_44610644/article/details/104821928)（事实上不需要用时间算，还容易出bug，算帧数就好）

写于 2021.8.17。

## 游戏玩法
类似Flappy Bird，不能接触水管，小鸟点击可跳跃。此外小鸟可以左右移动，添加了会反弹的物体、部分道具，不能接触添加的物体，可拾取道具。

水管每次只会出现一个。游戏目标不再是穿过更多的水管，而是坚持更长的时间。

**运行方式：**

运行目录中的`main.py`即可。

具体：命令行中输入`python`后加`main.py所在路径`，如`python "F:\Codes\Python\Flappy Bird v1.0\main.py"`。

**道具说明：**

钻石：当前得分加2秒。

冰瓜：使水管、物体减速，或使水管、物体短暂冻结。

能量豆：无敌4秒。

## 已实现的功能
1. 三种道具：钻石：加两秒的得分。冰瓜：减慢或短暂冻住运动的球，减慢水管移动速度。能量豆：获得4s无敌，当无敌时不能再拾取能量豆；出现的不会消失，但同一时间界面中只能存在一个（应该要砍，设定的太容易出现了）。
2. 道具音效/特效：拾取钻石的音效，冰瓜破碎的音效，冰冻效果的音效（寒冰射手/寒冰菇命中后的减速音效），碰撞效果及音效（pvz中植物爆炸效果及音效），无敌效果（高亮度+金光），无敌结束前闪烁效果。
3. 几乎完全还原Flappy Bird的操作手感，并添加新的挑战。

## 未完成的功能
1. 水管速度、球的速度、重力随游戏进行而增大，单次跳跃高度随游戏进行减小。考虑到游戏已经足够难，没有添加。其实已经记录了时间，只需要设计速度与时间的变化函数即可。
2. 添加冰冻时类似寒冰菇的全屏效果，目前考虑只是替换背景为带滤镜的背景，冰花的设计感觉有点难。
3. 优化游戏内文字内容显示。因为对文字不感兴趣，以及基本就自己玩，所以没改。

## 待添加的功能
1. 排行榜。
2. 难度选择，简单：只有水管，中等：水管+随机一个球，困难：水管+三个球。因为基本只有自己玩而且自己可以随便改，就没去加。
3. 关卡设计，将水管替换为设定的障碍，坚持躲避球指定时间过关。
4. 冰瓜拾取后碎裂效果。
5. GUI设计，还需要学pygame_menu。




