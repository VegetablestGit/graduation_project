from backpack_problem import *
import random
import numpy as np

def de_for_backpack(maxgen:int,problem:BackpackProblem)->List[float]: 
    pop_size = problem.len()
    x_list = np.random.random((pop_size,problem.len()))
    y = np.array([problem.calc_value(x) for x in x_list])
    best_value_list = [max(y)]
    for gen in range(maxgen):
        xr1 = np.array([random.choice(x_list)for _ in range(pop_size)])
        xr2 = np.array([random.choice(x_list)for _ in range(pop_size)])
        xr3 = np.array([random.choice(x_list)for _ in range(pop_size)])
        v = xr1 + 0.5*(xr2-xr3)
        u = np.array([x_list[i] if random.random()>0.5 else v[i] for i in range(pop_size)])
        uy = np.array([problem.calc_value(pos) for pos in u])
        x_list = [u[i]if uy[i]>y[i]else x_list[i]for i in range(pop_size)]
        y = np.maximum(uy,y)
        best_value_list.append(y.max())
    return best_value_list
        

