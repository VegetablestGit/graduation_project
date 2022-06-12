from knapsack_problem import KnapsackProBlem
import numpy as np
from typing import List

step_rate = 1.2
steps = []
left_value_list = []

def as_foa_for_knapsack(maxgen:int,init_step:float,problem:KnapsackProBlem)->List[float]: 
    pop_size = problem.len()
    i1 = pop_size//4
    i2 = pop_size//2
    i3 = i2 + pop_size//4
    step_left = init_step
    step_right = init_step
    pos_left = np.random.random(problem.len())
    pos_right = pos_left
    last_value_left = problem.calc_value_and_optimise(pos_left)
    best_value = last_value_left
    best_value_list = []
    left_value_list.clear()
    stop_times = 0
    steps.clear()
    stop_dict = {}
    left_cnt, right_cnt = 0, 0
    for gen in range(maxgen):
        steps.append(step_right)
        step_list = [step_left*step_rate]*i1 + [step_left/step_rate]*(i2-i1) + [step_right*step_rate]*(i3-i2)+[step_right/step_rate]*(pop_size-i3)
        pos_list = [random_fly(pos_left,s) for s in step_list[:i2]] + [random_fly(pos_right,s) for s in step_list[i2:]]
        value_list = [problem.calc_value_and_optimise(p) for p in pos_list]
        best_value_left = max(value_list[:i2])
        best_index_left = value_list[:i2].index(best_value_left)
        best_pos_left = pos_list[best_index_left]
        best_value_right = max(value_list[i2:])
        best_index_right = value_list[i2:].index(best_value_right) + i2
        best_pos_right = pos_list[best_index_right]
        #自适应更新step
        if best_index_left < i1:
            step_left *= step_rate
        else:
            step_left /= step_rate
        if best_index_right < i3:
            step_right *= step_rate
        else:
            step_right /= step_rate
        step_left = min(1.0,step_left)
        step_right = min(1.0,step_right)

        if best_value_left > best_value and best_value_left >= best_value_right:
            stop_times = 0
            pos_left, pos_right = best_pos_left,best_pos_left
            step_right = step_left
            left_cnt += 1
        elif best_value_right > best_value and best_value_right >= best_value_left:
            stop_times = 0
            pos_left, pos_right = best_pos_right,best_pos_right
            step_left = step_right
            right_cnt += 1
        else: #best_value_left <= best_value and best_value_right <= best_value
            if stop_times >= 10:
                if best_value_left not in stop_dict:
                    stop_dict[best_value_left] = 1
                else:
                    stop_dict[best_value_left] += 1
                pos_left = random_fly(pos_left,min(1.0,stop_dict[best_value_left]*0.05))
                stop_times = 0
            elif best_value_left <= last_value_left:
                stop_times += 1
                if best_value_left == last_value_left:
                    pos_left = best_pos_left
            else:
                stop_times = 0
                pos_left = best_pos_left

            if best_value_left == best_value:
                pos_right = best_pos_left
            elif best_value_right == best_value:
                pos_right = best_pos_right
        best_value = max(best_value,best_value_left,best_value_right)
        last_value_left = problem.calc_value_and_optimise(pos_left)
        best_value_list.append(best_value)
        left_value_list.append(last_value_left)
    return best_value_list

def random_fly(pos:np.ndarray,step:float,bound:float=1.0)->np.ndarray:
    return np.random.normal(pos,step).clip(-bound,bound)

def foa_for_knapsack(maxgen:int,step:float,problem:KnapsackProBlem):
    pop_size = problem.len()
    pos = np.random.random(problem.len())
    best_value = problem.calc(pos)
    best_value_list = [best_value]
    for gen in range(maxgen):
        pos_list = [random_fly(pos,step) for _ in range(pop_size)]
        value_list = [problem.calc(p) for p in pos_list]
        current_best_value = max(value_list)
        best_index = value_list.index(current_best_value)
        current_best_pos = pos_list[best_index]
        if current_best_value >= best_value:
            pos = current_best_pos
            best_value = current_best_value
        best_value_list.append(best_value)
    return best_value_list

def as_foa_for_func(maxgen:int,init_step:float,func,n_dim,bound:float,pop_size:int):
    steps.clear()
    # i1 = pop_size//4
    # i2 = pop_size//2
    # i3 = i2 + pop_size//4
    i1,i2,i3 = 0,0,pop_size//2
    step_left = init_step
    step_right = init_step
    pos_left = np.random.random(n_dim)*bound*2-bound
    pos_right = pos_left
    last_value_left = func(pos_left)
    best_value = last_value_left
    best_value_list = []
    left_value_list = []
    stop_times = 0
    stop_dict = {}
    stop_times_list = []
    for gen in range(maxgen):
        stop_times_list.append(stop_times)
        steps.append(step_right)
        step_list = [step_left*2]*i1 + [step_left/2]*(i2-i1) + [step_right*2]*(i3-i2)+[step_right/2]*(pop_size-i3)
        pos_list = [random_fly(pos_left,s,bound) for s in step_list[:i2]] + [random_fly(pos_right,s,bound) for s in step_list[i2:]]
        value_list = [func(p) for p in pos_list]
        # best_value_left = min(value_list[:i2])
        # best_index_left = value_list[:i2].index(best_value_left)
        # best_pos_left = pos_list[best_index_left]
        best_value_right = min(value_list[i2:])
        best_index_right = value_list[i2:].index(best_value_right) + i2
        best_pos_right = pos_list[best_index_right]
        #自适应更新step
        # if best_index_left < i1:
        #     step_left *= 1.25
        # else:
        #     step_left *= 0.8
        if best_index_right < i3:
            step_right *= 1.25
        else:
            step_right *= 0.8

        if best_value_right < best_value:
            pos_right = best_pos_right
        
        # stop_value = int(best_value_left*10**3)
        # if stop_times >= 10 or stop_value in stop_dict:
        #     if best_value_left not in stop_dict:
        #         stop_dict[stop_value] = 1
        #     else:
        #         stop_dict[stop_value] += 1
        #     pos_left = random_fly(pos_left,min(bound,bound/10*2**stop_dict[stop_value],bound))
        #     stop_times = 0
        # elif abs(last_value_left - best_value_left) < 10**-3:
        #     stop_times += 1
        # else:
        #     stop_times = 0
        # if best_value_left < best_value:
        #     pos_left, pos_right = best_pos_left,best_pos_left
        #     step_right = step_left
        # elif best_value_left < last_value_left:
        #     pos_left = best_pos_left
            
        
        #best_value = min(best_value,best_value_left,best_value_right)
        best_value = min(best_value,best_value_right)
        last_value_left = func(pos_left)
        best_value_list.append(best_value)
        left_value_list.append(last_value_left)
    return best_value_list

def foa_for_func(maxgen:int,step:float,func,n_dim,bound:float,pop_size:int):
    pos = np.random.random(n_dim)
    best_value = func(pos)
    best_value_list = [best_value]
    for gen in range(maxgen):
        pos_list = [random_fly(pos,step,bound) for _ in range(pop_size)]
        value_list = [func(p) for p in pos_list]
        current_best_value = min(value_list)
        best_index = value_list.index(current_best_value)
        current_best_pos = pos_list[best_index]
        if current_best_value < best_value:
            pos = current_best_pos
            best_value = current_best_value
        best_value_list.append(best_value)
    return best_value_list