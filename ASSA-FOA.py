
from cv2 import sumElems
from matplotlib.pyplot import summer
from backpack_problem import BackpackProblem
import random

from typing import List
def assa_foa_for_backpack(maxgen:int,init_step:float,pop_size:int,problem:BackpackProblem)->List[float]: 
    step = init_step
    y_list = []
    pos = [random.random() for _ in range(len(problem.items))]
    best_y = calc_value(pos,problem)
    last_y = best_y
    temp = 10000 #初始温度
    temp_d = 0.97 #温度衰减系数
    problem.sort()
    for gen in range(maxgen):
        #设置马尔科夫链长度为 最大迭代次数/100
        #温度一共衰减100次
        if (maxgen//100)%gen == 0:
            temp = temp * temp_d
        random_fly_pos = random_fly(pos,init_step)

        pos_set_m = [random_fly(pos,step) for _ in range(pop_size/3)]
        pos_set_s = [random_fly(pos,step/2) for _ in range(pop_size/3)]
        pos_set_l = [random_fly(pos,step*2) for _ in range(pop_size/3)]
        values_m = [calc_value(x_vec,problem) for x_vec in pos_set_m]
        weights_s = [calc_value(x_vec,problem) for x_vec in pos_set_s]
        weights_l = [calc_value(x_vec,problem) for x_vec in pos_set_l]
        best_index_m, best_weight_m = values_m.index(max(values_m)),max(values_m)
        best_index_s, best_weight_s = values_m.index(max(weights_s)),max(weights_s)
        best_index_l, best_weight_l = values_m.index(max(weights_l)),max(weights_l)
        
        
#计算重量并优化pos 多退少补
def calc_value(pos:List[float],problem:BackpackProblem)->float:
    value = 0
    weight = 0
    for i,x in enumerate(pos):
        if select(x):
            value += problem.items[i].value
            weight += problem.items[i].weight

    if weight > problem.weight_limit: #多退
        for i,x in enumerate(pos): 
            if select(x):
                pos[i] = 0.49
                weight -= problem.items[i].weight
                value -= problem.items[i].value
            if weight <= problem.weight_limit:
                return value
    else: #少补
        for i,x in enumerate(pos): 
            if not select(x) and weight + problem.items[i].weight <= problem.weight_limit:
                pos[i] = 0.51
                weight += problem.items[i].weight
                value += problem.items[i].value
            if weight + problem.items[i].weight > problem.weight_limit:
                return value
    return value

def select(x:float)->bool:
    return x >= 0.5

def random_fly(pos:List[float],step:float)->List[float]:
    return [min(1,max(0,x+random.uniform(-step,step))) for x in pos]