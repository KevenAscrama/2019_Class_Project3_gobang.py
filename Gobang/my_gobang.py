#!/usr/bin/env python3
from graphics import *
from math import *
import numpy as np


#参数列表

GRID_WIDTH = 40

COLUMN = 15
ROW = 15

list1 = []  # AI
list2 = []  # human
list3 = []  # all

list_all = []  # 整个棋盘的点
next_point = [0, 0]  # AI下一步最应该下的位置

ratio = 1  # 进攻的系数   大于1 进攻型，  小于1 防守型
DEPTH = 3  # 搜索深度   只能是单数。  如果是负数， 评估函数评估的的是自己多少步之后的自己得分的最大值，并不意味着是最好的棋， 评估函数的问题


# 棋型的评估分数,1表示有子,0表示无子
# TODO:以下为举例用的棋形评估分数，可以自己扩展与改分
################################# here ##################################
# 给出评价
shape_score = [
               (50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),

               (200, (1, 1, 0, 1, 0)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),
               (5000, (0, 1, 1, 1, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),

               (5000, (1, 1, 1, 0, 1)),
               (5000, (1, 1, 0, 1, 1)),
               (5000, (1, 0, 1, 1, 1)),
               (5000, (1, 1, 1, 1, 0)),
               (5000, (0, 1, 1, 1, 1)),
               (50000, (0, 1, 1, 1, 1, 0)),
               (99999999, (1, 1, 1, 1, 1))
              ]

shape_score2 = [
               # (50, (0, 1, 1, 0, 0)),
               # (50, (0, 0, 1, 1, 0)),

               # (200, (1, 1, 0, 1, 0)),
               # (500, (0, 0, 1, 1, 1)),
               # (500, (1, 1, 1, 0, 0)),
               # (5000, (0, 1, 1, 1, 0)),
               # (5000, (0, 1, 0, 1, 1, 0)),
               # (5000, (0, 1, 1, 0, 1, 0)),

               # (5000, (1, 1, 1, 0, 1)),
               # (5000, (1, 1, 0, 1, 1)),
               # (5000, (1, 0, 1, 1, 1)),
               # (5000, (1, 1, 1, 1, 0)),
               # (5000, (0, 1, 1, 1, 1)),
               # (50000, (0, 1, 1, 1, 1, 0)),
               # (99999999, (1, 1, 1, 1, 1))

               (50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),

               (500, (1, 1, 1, 0, 0)),
               (2000, (0, 1, 1, 1, 0)),
               (500, (0, 0, 1, 1, 1)),

               (200, (1, 1, 0, 1, 0)),
               (1000, (0, 1, 0, 1, 1, 0)),
               (1000, (0, 1, 1, 0, 1, 0)), 

               (5000, (1, 1, 1, 1, 0)),
               (5000, (1, 1, 1, 0, 1)),
               (8000, (1, 1, 0, 1, 1)),
               (5000, (1, 0, 1, 1, 1)),
               (10000, (0, 1, 1, 1, 1)),
               (50000, (0, 1, 1, 1, 1, 0)),
               (99999999, (1, 1, 1, 1, 1))


               # ,(-50, (0, 2, 2, 0, 0)),
               # (-50, (0, 0, 2, 2, 0)),
               # (-200, (2, 2, 0, 2, 0)),
               # (-500, (0, 0, 2, 2, 2)),
               # (-500, (2, 2, 2, 0, 0)),
               # (-5000, (0, 2, 2, 2, 0)),
               # (-5000, (0, 2, 0, 2, 2, 0)),
               # (-5000, (0, 2, 2, 0, 2, 0)),
               # (-5000, (2, 2, 2, 0, 2)),
               # (-5000, (2, 2, 0, 2, 2)),
               # (-5000, (2, 0, 2, 2, 2)),
               # (-5000, (2, 2, 2, 2, 0)),
               # (-5000, (0, 2, 2, 2, 2)),
               # (-50000, (0, 2, 2, 2, 2, 0)),
               # (-99999999, (2, 2, 2, 2, 2))

               # ,(-50, (0, -1, -1, 0, 0)),
               # (-50, (0, 0, -1, -1, 0)),
               # (-200, (-1, -1, 0, -1, 0)),
               # (-500, (0, 0, -1, -1, -1)),
               # (-500, (-1, -1, -1, 0, 0)),
               # (-5000, (0, -1, -1, -1, 0)),
               # (-5000, (0, -1, 0, -1, -1, 0)),
               # (-5000, (0, -1, -1, 0, -1, 0)),
               # (-5000, (-1, -1, -1, 0, -1)),
               # (-5000, (-1, -1, 0, -1, -1)),
               # (-5000, (-1, 0, -1, -1, -1)),
               # (-5000, (-1, -1, -1, -1, 0)),
               # (-5000, (0, -1, -1, -1, -1)),
               # (-50000, (0, -1, -1, -1, -1, 0)),
               # (-99999999, (-1, -1, -1, -1, -1))
               ]


def ai_step():
	'''
	AI下一步棋判断
	:return: next_point
	'''
    ################################### here ########################
	# count the number of cuts
	global cnt_cut
	cnt_cut = 0
	# count the number of searches
	global cnt_search
	cnt_search = 0

	negamax(True, DEPTH, -99999999, 99999999)

	print("Total cut counts：\t" + str(cnt_cut))
	print("Total search counts \t" + str(cnt_search))

	return next_point[0], next_point[1]


# alpha beta 剪枝
def negamax(is_ai, depth, alpha, beta):
    '''
    负值极大算法搜索 alpha + beta剪枝
    :param is_ai: 是否是ai轮
    :param depth: 搜索深度
    :return: alpha or beta（需要补全）
    '''
    # 游戏是否结束 | | 探索的递归深度是否到边界
    if game_win(list1) or game_win(list2) or depth == 0:
        return evaluation(is_ai)

    blank_list = list(set(list_all).difference(set(list3)))
    order(blank_list)   # 搜索顺序排序  提高剪枝效率
    # TODO: 对每一个候选步进行递归并剪枝，将最后决策出的next_point赋值，将函数剩下部分补全
    # .....
    
    ################################### here ######################################
 	#try all the steps
    for step in blank_list:

        global cnt_search
        cnt_search += 1

        # if no neighbour around, skip this step. 
        if not has_neightnor(step):
            continue

        # add this step to lists. 
        if is_ai:
            list1.append(step) #list 1 is for AI
        else:
            list2.append(step)# list 2 is for Human
        list3.append(step)

        # compute the negative max with this step in count.
        ############################################################
        ret = -negamax(not is_ai, depth - 1, -beta, -alpha) # recursive funciton. 
		    ############################################################
        # remove this step
        if is_ai:
            list1.remove(step)
        else:
            list2.remove(step)
        list3.remove(step)

        # if this ret is bigger than alpha
        if ret > alpha:
            print(str(ret) + "\t alpha:" + str(alpha) + "\t beta:" + str(beta))
            # print(list3)
            if depth == DEPTH: # search depth is set for 3. 
                next_point[0] = step[0]
                next_point[1] = step[1]

            # start alpha-beta cut
            if ret >= beta:
                global cnt_cut
                cnt_cut += 1
                return beta

            alpha = ret
    return alpha




def order(blank_list):
	'''
	离最后落子的邻居位置最有可能是最优点，策略优化，无需改动
	'''
	last_pt = list3[-1]
	for item in blank_list:
	    for i in range(-1, 2):
	        for j in range(-1, 2):
	            if i == 0 and j == 0:
	                continue
	            if (last_pt[0] + i, last_pt[1] + j) in blank_list:
	                blank_list.remove((last_pt[0] + i, last_pt[1] + j))
	                blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))


def has_neightnor(pt):
	'''
	查看某个位置是否有邻居，用于剪枝
	:param pt:
	:return:
	'''
	for i in range(-1, 2):
	    for j in range(-1, 2):
	        if i == 0 and j == 0:
	            continue
	        if (pt[0] + i, pt[1]+j) in list3:
	            return True
	return False


# 评估函数
def evaluation(is_ai):
	'''
	评估函数，用于评估当前棋盘局势
	:param is_ai:是否是AI的评估
	:return:当前棋局博弈双方的总分
	'''
	total_score = 0

	if is_ai:
	    my_list = list1
	    enemy_list = list2
	else:
	    my_list = list2
	    enemy_list = list1

	# 算自己的得分
	score_all_arr = []  # 得分形状的位置 用于计算如果有相交 得分翻倍
	my_score = 0
	for pt in my_list:
	    m = pt[0]
	    n = pt[1]
	    my_score += cal_score(m, n, 0, 1, enemy_list, my_list, score_all_arr)
	    my_score += cal_score(m, n, 1, 0, enemy_list, my_list, score_all_arr)
	    my_score += cal_score(m, n, 1, 1, enemy_list, my_list, score_all_arr)
	    my_score += cal_score(m, n, -1, 1, enemy_list, my_list, score_all_arr)

	#  算敌人的得分， 并减去
	score_all_arr_enemy = []
	enemy_score = 0
	for pt in enemy_list:
	    m = pt[0]
	    n = pt[1]
	    enemy_score += cal_score(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
	    enemy_score += cal_score(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
	    enemy_score += cal_score(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
	    enemy_score += cal_score(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)

	total_score = my_score - enemy_score*ratio*0.1

	return total_score


# 每个方向上的分值计算
# 查看其某一指定方向上的棋形，并根据shape_score对棋形进行打分
def cal_score(m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr):
    '''
    计算(m,n)点的指定方向上棋盘形状的评估分值
    :param m: x坐标值
    :param n: y坐标值
    :param x_decrict:指定x轴方向
    :param y_derice:指定y轴方向
    :param enemy_list:对手的棋局
    :param my_list:我方的棋局
    :param score_all_arr:得分形状的位置，用于计算是否有有相交，如果有则得分翻倍
    :return: 当前方向上的得分
    '''
    add_score = 0  # 加分项
    # 在一个方向上， 只取最大的得分项
    max_score_shape = (0, None)

    # 如果此方向上，该点已经有得分形状，不重复计算
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0

    # TODO: 在落子点指定方向上查找形状，并根据shape_score计分，将最大的score值与其对应shape赋值给max_score_shape,在END前补齐代码
    # ......
    ################################# here #################################
	# find the shape in specific direction left or right using double loop. 
	# put is from -5 to 0
    for put in range(-5, 1):
        position = []
        # get the current shape
        # i is from 0 to 5
        for i in range(0, 6):
        	  # if the point is enemy's
        	  # i+put is from -5 to 5 which means from search from left to right. 
            if (m + (i + put) * x_decrict, n + (i + put) * y_derice) in enemy_list:
                position.append(2)

            # if it is mine
            elif (m + (i + put) * x_decrict, n + (i + put) * y_derice) in my_list:
                position.append(1)

            # if the point is empty
            else:
                position.append(0)

        # shape1 has 5 points
        shape1 = (position[0], position[1], position[2], position[3], position[4])
        # shape2 has 6 points
        shape2 = (position[0], position[1], position[2], position[3], position[4], position[5])

        for (score, shape) in shape_score:
        	# find the score that matches the current shape
            if shape1 == shape or shape2 == shape:
                # if current score is the best score, put it into the max score shape
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0+put) * x_decrict, n + (0+put) * y_derice),
                                               (m + (1+put) * x_decrict, n + (1+put) * y_derice),
                                               (m + (2+put) * x_decrict, n + (2+put) * y_derice),
                                               (m + (3+put) * x_decrict, n + (3+put) * y_derice),
                                               (m + (4+put) * x_decrict, n + (4+put) * y_derice)), 
                                               (x_decrict, y_derice)
                                               )

    # END     

    # 计算两个形状相交， 如两个3活 相交， 得分增加 一个子的除外
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]

        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0]




############################# AI NO.2 ##################################

def ai_step2():
  '''
  AI下一步棋判断
  :return: next_point
  '''
    ################################### here ########################
  # count the number of cuts
  global cnt_cut
  cnt_cut = 0
  # count the number of searches
  global cnt_search
  cnt_search = 0

  negamax2(True, DEPTH, -99999999, 99999999)

  print("Total cut counts：\t" + str(cnt_cut))
  print("Total search counts \t" + str(cnt_search))

  return next_point[0], next_point[1]




def negamax2(is_ai, depth, alpha, beta):
    '''
    负值极大算法搜索 alpha + beta剪枝
    :param is_ai: 是否是ai轮
    :param depth: 搜索深度
    :return: alpha or beta（需要补全）
    '''
    # 游戏是否结束 | | 探索的递归深度是否到边界
    if game_win(list1) or game_win(list2) or depth == 0:
        return evaluation2(is_ai)

    blank_list = list(set(list_all).difference(set(list3)))
    order(blank_list)   # 搜索顺序排序  提高剪枝效率
    # TODO: 对每一个候选步进行递归并剪枝，将最后决策出的next_point赋值，将函数剩下部分补全
    # .....
    
    ################################### here ######################################
  #try all the steps
    for step in blank_list:

        global cnt_search
        cnt_search += 1

        # if no neighbour around, skip this step. 
        if not has_neightnor(step):
            continue

        # add this step to lists. 
        if is_ai:
            list2.append(step) #list 1 is for AI
        else:
            list1.append(step)# list 2 is for Human
        list3.append(step)

        # compute the negative max with this step in count.
        ############################################################
        ret = -negamax2(not is_ai, depth - 1, -beta, -alpha) # recursive funciton. 
        ############################################################
        # remove this step
        if is_ai:
            list2.remove(step)
        else:
            list1.remove(step)
        list3.remove(step)

        # if this ret is bigger than alpha
        if ret > alpha:
            print(str(ret) + "\t alpha:" + str(alpha) + "\t beta:" + str(beta))
            # print(list3)
            if depth == DEPTH: # search depth is set for 3. 
                next_point[0] = step[0]
                next_point[1] = step[1]

            # start alpha-beta cut
            if ret >= beta:
                global cnt_cut
                cnt_cut += 1
                return beta

            alpha = ret
    return alpha





def evaluation2(is_ai):
  '''
  评估函数，用于评估当前棋盘局势
  :param is_ai:是否是AI的评估
  :return:当前棋局博弈双方的总分
  '''
  total_score = 0

  if is_ai:
      my_list = list2
      enemy_list = list1
  else:
      my_list = list1
      enemy_list = list2

  # 算自己的得分
  score_all_arr = []  # 得分形状的位置 用于计算如果有相交 得分翻倍
  my_score = 0
  for pt in my_list:
      m = pt[0]
      n = pt[1]
      my_score += cal_score2(m, n, 0, 1, enemy_list, my_list, score_all_arr)
      my_score += cal_score2(m, n, 1, 0, enemy_list, my_list, score_all_arr)
      my_score += cal_score2(m, n, 1, 1, enemy_list, my_list, score_all_arr)
      my_score += cal_score2(m, n, -1, 1, enemy_list, my_list, score_all_arr)

  #  算敌人的得分， 并减去
  score_all_arr_enemy = []
  enemy_score = 0
  for pt in enemy_list:
      m = pt[0]
      n = pt[1]
      enemy_score += cal_score2(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
      enemy_score += cal_score2(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
      enemy_score += cal_score2(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
      enemy_score += cal_score2(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)

  total_score = my_score - enemy_score*ratio*0.1

  return total_score


def cal_score2(m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr):
    '''
    计算(m,n)点的指定方向上棋盘形状的评估分值
    :param m: x坐标值
    :param n: y坐标值
    :param x_decrict:指定x轴方向
    :param y_derice:指定y轴方向
    :param enemy_list:对手的棋局
    :param my_list:我方的棋局
    :param score_all_arr:得分形状的位置，用于计算是否有有相交，如果有则得分翻倍
    :return: 当前方向上的得分
    '''
    add_score = 0  # 加分项
    # 在一个方向上， 只取最大的得分项
    max_score_shape = (0, None)

    # 如果此方向上，该点已经有得分形状，不重复计算
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0

    # TODO: 在落子点指定方向上查找形状，并根据shape_score计分，将最大的score值与其对应shape赋值给max_score_shape,在END前补齐代码
    # ......
    ################################# here #################################
  # find the shape in specific direction left or right using double loop. 
  # put is from -5 to 0
    for put in range(-5, 1):
        position = []
        # get the current shape
        # i is from 0 to 5
        for i in range(0, 6):
            # if the point is enemy's
            # i+put is from -5 to 5 which means from search from left to right. 
            if (m + (i + put) * x_decrict, n + (i + put) * y_derice) in enemy_list:
                position.append(2)

            # if it is mine
            elif (m + (i + put) * x_decrict, n + (i + put) * y_derice) in my_list:
                position.append(1)

            # if the point is empty
            else:
                position.append(0)

        # shape1 has 5 points
        shape1 = (position[0], position[1], position[2], position[3], position[4])
        # shape2 has 6 points
        shape2 = (position[0], position[1], position[2], position[3], position[4], position[5])

        for (score, shape) in shape_score2:
          # find the score that matches the current shape
            if shape1 == shape or shape2 == shape:
                # if current score is the best score, put it into the max score shape
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0+put) * x_decrict, n + (0+put) * y_derice),
                                               (m + (1+put) * x_decrict, n + (1+put) * y_derice),
                                               (m + (2+put) * x_decrict, n + (2+put) * y_derice),
                                               (m + (3+put) * x_decrict, n + (3+put) * y_derice),
                                               (m + (4+put) * x_decrict, n + (4+put) * y_derice)), 
                                               (x_decrict, y_derice)
                                               )

    # END     

    # 计算两个形状相交， 如两个3活 相交， 得分增加 一个子的除外
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]

        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0]


def game_win(list):
	'''
	传入的list判断当前list是否已经连出五子
	:param list:需要判断的棋子列表
	:return: True or False
	'''
	for m in range(COLUMN):
	    for n in range(ROW):

	        if n < ROW - 4 and (m, n) in list and (m, n + 1) in list and (m, n + 2) in list and (
	                m, n + 3) in list and (m, n + 4) in list:
	            return True
	        elif m < ROW - 4 and (m, n) in list and (m + 1, n) in list and (m + 2, n) in list and (
	                    m + 3, n) in list and (m + 4, n) in list:
	            return True
	        elif m < ROW - 4 and n < ROW - 4 and (m, n) in list and (m + 1, n + 1) in list and (
	                    m + 2, n + 2) in list and (m + 3, n + 3) in list and (m + 4, n + 4) in list:
	            return True
	        elif m < ROW - 4 and n > 3 and (m, n) in list and (m + 1, n - 1) in list and (
	                    m + 2, n - 2) in list and (m + 3, n - 3) in list and (m + 4, n - 4) in list:
	            return True
	return False


def gobangwin():
	''' 绘制基本棋盘界面 '''
	win = GraphWin("this is a gobang game", GRID_WIDTH * COLUMN, GRID_WIDTH * ROW)
	win.setBackground("yellow")
	i1 = 0

	while i1 <= GRID_WIDTH * COLUMN:
	    l = Line(Point(i1, 0), Point(i1, GRID_WIDTH * COLUMN))
	    l.draw(win)
	    i1 = i1 + GRID_WIDTH
	i2 = 0

	while i2 <= GRID_WIDTH * ROW:
	    l = Line(Point(0, i2), Point(GRID_WIDTH * ROW, i2))
	    l.draw(win)
	    i2 = i2 + GRID_WIDTH
	return win


def main_AI():
	''' 人机对战函数 '''
	win = gobangwin()

	for i in range(COLUMN+1):
	    for j in range(ROW+1):
	        list_all.append((i, j))

	change = 0
	g = 0
	m = 0
	n = 0

	while g == 0:

		if change % 2 == 0: #黑子
			p2 = win.getMouse()
			if not ((round((p2.getX()) / GRID_WIDTH), round((p2.getY()) / GRID_WIDTH)) in list3):
				a2 = round((p2.getX()) / GRID_WIDTH)
				b2 = round((p2.getY()) / GRID_WIDTH)
				list2.append((a2, b2))
				list3.append((a2, b2))

				piece = Circle(Point(GRID_WIDTH * a2, GRID_WIDTH * b2), 16)
				piece.setFill('black')
				piece.draw(win)
				if game_win(list2):
				    message = Text(Point(100, 100), "black win.")
				    message.draw(win)
				    g = 1

				change = change + 1

		elif change % 2 == 1 :#白子
		    pos = ai_step()

		    if pos in list3:
		        message = Text(Point(200, 200), "不可用的位置" + str(pos[0]) + "," + str(pos[1]))
		        message.draw(win)
		        g = 1

		    list1.append(pos)
		    list3.append(pos)

		    piece = Circle(Point(GRID_WIDTH * pos[0], GRID_WIDTH * pos[1]), 16)
		    piece.setFill('white')
		    piece.draw(win)

		    if game_win(list1):
		        message = Text(Point(100, 100), "white win.")
		        message.draw(win)
		        g = 1
		    change = change + 1
	        
	message = Text(Point(100, 120), "Click anywhere to quit.")
	message.draw(win)
	win.getMouse()
	win.close()



def main_Human():
    ''' 人人对战函数 '''
    win = gobangwin()

    for i in range(COLUMN + 1):
        for j in range(ROW + 1):
            list_all.append((i, j))

    change = 0
    g = 0
    while g == 0:

        p = win.getMouse()

        if change % 2 ==0 : # 黑子
            if not ((round((p.getX()) / GRID_WIDTH), round((p.getY()) / GRID_WIDTH)) in list3):

                a = round((p.getX()) / GRID_WIDTH)
                b = round((p.getY()) / GRID_WIDTH)
                list1.append((a, b))
                list3.append((a, b))

                piece = Circle(Point(GRID_WIDTH * a, GRID_WIDTH * b), 16)
                piece.setFill('black')
                piece.draw(win)
                if game_win(list1):
                    message = Text(Point(100, 100), "black win.")
                    message.draw(win)
                    g = 1

                change = change + 1

        elif change % 2 == 1: # 白子
            if not ((round((p.getX()) / GRID_WIDTH), round((p.getY()) / GRID_WIDTH)) in list3):

                a = round((p.getX()) / GRID_WIDTH)
                b = round((p.getY()) / GRID_WIDTH)
                list2.append((a, b))
                list3.append((a, b))

                piece = Circle(Point(GRID_WIDTH * a, GRID_WIDTH * b), 16)
                piece.setFill('white')
                piece.draw(win)
                if game_win(list2):
                    message = Text(Point(100, 100), "White win.")
                    message.draw(win)
                    g = 1

                change = change + 1

    message = Text(Point(100, 120), "Click anywhere to quit.")
    message.draw(win)
    win.getMouse()
    win.close()

def main_AI_fight_AI2first():
  ''' 机机对战函数 '''


  win = gobangwin()

  for i in range(COLUMN+1):
      for j in range(ROW+1):
          list_all.append((i, j))

  change = 0


  g = 0
  m = 0
  n = 0

  if change % 2 == 0: #黑子
      p2 = win.getMouse()
      if not ((round((p2.getX()) / GRID_WIDTH), round((p2.getY()) / GRID_WIDTH)) in list3):
        a2 = round((p2.getX()) / GRID_WIDTH)
        b2 = round((p2.getY()) / GRID_WIDTH)
        list2.append((a2, b2))
        list3.append((a2, b2))

        piece = Circle(Point(GRID_WIDTH * a2, GRID_WIDTH * b2), 16)
        piece.setFill('black')
        piece.draw(win)
        if game_win(list2):
            message = Text(Point(100, 100), "black win.")
            message.draw(win)
            g = 1

        change = change + 1


  while g == 0:

    if change % 2 == 0: #黑子 AI2

        pos = ai_step2()

        if pos in list3:
            message = Text(Point(200, 200), "不可用的位置" + str(pos[0]) + "," + str(pos[1]))
            message.draw(win)
            g = 1

        list2.append(pos)
        list3.append(pos)

        piece = Circle(Point(GRID_WIDTH * pos[0], GRID_WIDTH * pos[1]), 16)
        piece.setFill('black')
        piece.draw(win)

        if game_win(list2):
            message = Text(Point(100, 100), "black win.")
            message.draw(win)
            g = 1
        change = change + 1

    elif change % 2 == 1 :#白子
        pos = ai_step()

        if pos in list3:
            message = Text(Point(200, 200), "不可用的位置" + str(pos[0]) + "," + str(pos[1]))
            message.draw(win)
            g = 1

        list1.append(pos)
        list3.append(pos)

        piece = Circle(Point(GRID_WIDTH * pos[0], GRID_WIDTH * pos[1]), 16)
        piece.setFill('white')
        piece.draw(win)

        if game_win(list1):
            message = Text(Point(100, 100), "white win.")
            message.draw(win)
            g = 1
        change = change + 1
          
  message = Text(Point(100, 120), "Click anywhere to quit.")
  message.draw(win)
  win.getMouse()
  win.close()


def main_AI_fight_AI1first():
  ''' 机机对战函数 '''


  win = gobangwin()

  for i in range(COLUMN+1):
      for j in range(ROW+1):
          list_all.append((i, j))

  change = 0


  g = 0
  m = 0
  n = 0

  if change % 2 == 0: #黑子
      p2 = win.getMouse()
      if not ((round((p2.getX()) / GRID_WIDTH), round((p2.getY()) / GRID_WIDTH)) in list3):
        a2 = round((p2.getX()) / GRID_WIDTH)
        b2 = round((p2.getY()) / GRID_WIDTH)
        list2.append((a2, b2))
        list3.append((a2, b2))

        piece = Circle(Point(GRID_WIDTH * a2, GRID_WIDTH * b2), 16)
        piece.setFill('black')
        piece.draw(win)
        if game_win(list2):
            message = Text(Point(100, 100), "black win.")
            message.draw(win)
            g = 1

        change = change + 1


  while g == 0:

    if change % 2 == 0: #黑子 AI2

        pos = ai_step()

        if pos in list3:
            message = Text(Point(200, 200), "不可用的位置" + str(pos[0]) + "," + str(pos[1]))
            message.draw(win)
            g = 1

        list2.append(pos)
        list3.append(pos)

        piece = Circle(Point(GRID_WIDTH * pos[0], GRID_WIDTH * pos[1]), 16)
        piece.setFill('black')
        piece.draw(win)

        if game_win(list2):
            message = Text(Point(100, 100), "black win.")
            message.draw(win)
            g = 1
        change = change + 1

    elif change % 2 == 1 :#白子
        pos = ai_step2()

        if pos in list3:
            message = Text(Point(200, 200), "不可用的位置" + str(pos[0]) + "," + str(pos[1]))
            message.draw(win)
            g = 1

        list1.append(pos)
        list3.append(pos)

        piece = Circle(Point(GRID_WIDTH * pos[0], GRID_WIDTH * pos[1]), 16)
        piece.setFill('white')
        piece.draw(win)

        if game_win(list1):
            message = Text(Point(100, 100), "white win.")
            message.draw(win)
            g = 1
        change = change + 1
          
  message = Text(Point(100, 120), "Click anywhere to quit.")
  message.draw(win)
  win.getMouse()
  win.close()


if __name__ == '__main__':
	#main_AI();
	#main_Human();
  #main_AI_fight_AI2first();
  main_AI_fight_AI1first();
