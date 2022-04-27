from backpack_problem import BackpackProblem
import numpy as np
from typing import List

def as_foa_for_backpack(maxgen:int,init_step:float,pop_size:int,problem:BackpackProblem)->List[float]: 
    pop_size = problem.len()
    i1 = pop_size//4
    i2 = pop_size//2
    i3 = i2 + pop_size//4
    step_left = init_step
    step_right = init_step
    pos_left = np.random.random(problem.len())
    pos_left = np.zeros_like(pos_left)
    pos_right = pos_left
    last_value_left = problem.calc_value(pos_left)
    best_value = last_value_left
    best_value_list = []
    left_value_list = []
    stop_times = 0
    steps = []
    stop_dict = {}
    left_cnt, right_cnt = 0, 0
    for gen in range(maxgen):
        steps.append(step_left)
        step_list = [step_left*2]*i1 + [step_left/2]*(i2-i1) + [step_right*2]*(i3-i2)+[step_right/2]*(pop_size-i3)
        pos_list = [random_fly(pos_left,s) for s in step_list[:i2]] + [random_fly(pos_right,s) for s in step_list[i2:]]
        value_list = [problem.calc_value(p) for p in pos_list]
        best_value_left = max(value_list[:i2])
        best_index_left = value_list[:i2].index(best_value_left)
        best_pos_left = pos_list[best_index_left]
        best_value_right = max(value_list[i2:])
        best_index_right = value_list[i2:].index(best_value_right) + i2
        best_pos_right = pos_list[best_index_right]
        #自适应更新step
        if best_value_left > last_value_left:
            if best_index_left < i1:
                step_left *= 1.25
            else:
                step_left *= 0.8
        if best_value_right > best_value:
            if best_index_right < i3:
                step_right *= 1.25
            else:
                step_right *= 0.8
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
                pos_left = random_fly(pos_left,min(1.0,stop_dict[best_value_left]*0.1))
                stop_times = 0
            elif best_value_left <= last_value_left:
                stop_times += 1
                if best_value_left == last_value_left:
                    pos_left = best_pos_left
            else:
                stop_times = 0
                pos_left = best_pos_left

            if best_value_right == best_value:
                pos_right = pos_list[best_index_right]
        best_value = max(best_value,best_value_left,best_value_right)
        last_value_left = problem.calc_value(pos_left)
        best_value_list.append(best_value)
        left_value_list.append(last_value_left)
    #print("left stop avg:",sum(steps)/len(steps))
    #return best_value_list
    #print("left_cnt:",left_cnt," right_cnt:",right_cnt)
    return left_value_list

def random_fly(pos:np.ndarray,step:float)->np.ndarray:
    return (pos + np.random.uniform(-step,step,len(pos))).clip(0,1)