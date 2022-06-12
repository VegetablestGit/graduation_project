import knapsack_problem
import numpy as np
import sko

def get_func(problem:knapsack_problem.KnapsackProBlem):
    def func(pos):
        return -problem.calc(pos)
    return func
    

def de_for_knapsack(problem:knapsack_problem.KnapsackProBlem,maxgen):
    de = sko.DE.DE(func=get_func(problem),n_dim=problem.len(),size_pop=problem.len(),max_iter=maxgen)
    de.run()
    return np.array(de.generation_best_Y)*-1

def ga_for_knapsack(problem:knapsack_problem.KnapsackProBlem,maxgen):
    ga = sko.GA.GA(func=get_func(problem),n_dim=problem.len(),size_pop=problem.len(),max_iter=maxgen)
    ga.run()
    return np.array(ga.generation_best_Y)*-1

def pso_for_knapsack(problem:knapsack_problem.KnapsackProBlem,maxgen):
    pso = sko.PSO.PSO(func=get_func(problem),n_dim=problem.len(),pop=problem.len(),max_iter=maxgen)
    pso.run()
    return np.array(pso.gbest_y_hist).flatten()*-1

def de_for_func(func,n_dim,bound,maxgen,size_pop):
    de = sko.DE.DE(func,n_dim,size_pop = size_pop,lb=[-bound]*n_dim,ub=[bound]*n_dim,max_iter=maxgen)
    de.run()
    return np.array(de.generation_best_Y)

def ga_for_func(func,n_dim,bound,maxgen,size_pop):
    ga = sko.GA.GA(func,n_dim,size_pop = size_pop,lb=[-bound]*n_dim,ub=[bound]*n_dim,max_iter=maxgen)
    ga.run()
    return np.array(ga.generation_best_Y)

def pso_for_func(func,n_dim,bound,maxgen,size_pop):
    pso = sko.PSO.PSO(func,n_dim,pop = size_pop,lb=[-bound]*n_dim,ub=[bound]*n_dim,max_iter=maxgen,w=0.8, c1=0.5, c2=0.5)
    pso.run()
    return np.array(pso.gbest_y_hist).flatten()
    