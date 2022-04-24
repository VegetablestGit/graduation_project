
from backpack_problem import BackpackProblem
import random

from typing import List
def as_foa_for_backpack(maxgen:int,init_step:float,pop_size:int,problem:BackpackProblem)->List[float]: 
    problem.sort()
    step = init_step
    best_value_list = []
    pos = [random.random() for _ in range(len(problem.items))]
    last_value = calc_value(pos,problem)
    best_value = last_value
    #problem.sort()
    stop_times = 0
    steps = []
    stop_dict = {}
    for gen in range(maxgen):
        steps.append(step)
        
        pos_set_m = [random_fly(pos,step) for _ in range(pop_size//3)]
        pos_set_s = [random_fly(pos,step/2) for _ in range(pop_size//3)]
        pos_set_l = [random_fly(pos,step*2) for _ in range(pop_size//3)]
        values_m = [calc_value(x_vec,problem) for x_vec in pos_set_m]
        values_s = [calc_value(x_vec,problem) for x_vec in pos_set_s]
        values_l = [calc_value(x_vec,problem) for x_vec in pos_set_l]
        best_index_m, best_value_m = values_m.index(max(values_m)),max(values_m)
        best_index_s, best_value_s = values_s.index(max(values_s)),max(values_s)
        best_index_l, best_value_l = values_l.index(max(values_l)),max(values_l)
        temp_best_value = max(best_value_l,best_value_m,best_value_s)
        if temp_best_value == best_value_l:
            temp_best_pos = pos_set_l[best_index_l]
            step *= 1.2
        elif temp_best_value == best_value_s:
            temp_best_pos = pos_set_s[best_index_s]
            step *= 0.8
        else:
            temp_best_pos = pos_set_m[best_index_m]
        
        
        if temp_best_value <= last_value:
            if temp_best_value in stop_dict:
                stop_dict[temp_best_value] += 1
                pos = random_fly(pos,stop_dict[temp_best_value]*0.05)
            if max(best_value_l,best_value_m,best_value_s) == last_value:
                pos = temp_best_pos
            stop_times += 1
            if stop_times > 15:
                stop_dict[temp_best_value] = 0
                stop_times = 0
            continue
        pos = temp_best_pos
        best_value = max(best_value,temp_best_value)
        best_value_list.append(best_value)
        last_value = temp_best_value
        
    return best_value_list

        
        
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
        for i,x in enumerate(reversed(pos)): 
            if not select(x) and weight + problem.items[i].weight <= problem.weight_limit:
                pos[i] = 0.51
                weight += problem.items[i].weight
                value += problem.items[i].value
    return value

def select(x:float)->bool:
    return x >= 0.5

def random_fly(pos:List[float],step:float)->List[float]:
    return [min(1,max(0,x+random.uniform(-step,step))) for x in pos]