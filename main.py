import math
from pickletools import optimize
import knapsack_problem
import as_foa
import matplotlib.pyplot as plt
import os
import algos
import numpy as np
import funcs

best_values = [295.3,1024,3069,8362,5183,15170,2397,2460]
maxgen = 1000

def get_max_value_prefix(values):
    max_value = values[0]
    max_values = []
    for v in values:
        max_value = max(max_value,v)
        max_values.append(max_value)
    return max_values

def get_min_value_prefix(values):
    max_value = values[0]
    max_values = []
    for v in values:
        max_value = min(max_value,v)
        max_values.append(max_value)
    return max_values

n_dim = 10


if __name__ == "__main__":
    plt.figure(figsize=(6,4),dpi=300)
    problems = knapsack_problem.read_knapsack_problems()
    
    as_foa_values = [[]for _ in range(len(problems))]
    foa_values = [[]for _ in range(len(problems))]
    de_values = [[]for _ in range(len(problems))]
    ga_values = [[]for _ in range(len(problems))]
    pso_values = [[]for _ in range(len(problems))]
    for t in range(10):
        os.makedirs("output/%d"%(t+1),exist_ok=True)
        for i,problem in enumerate(problems):
            # if i!=7:
            #     continue
            plt.cla()
            plt.xlabel('iterate times')
            plt.ylabel('value')
            plt.title('data set %d'%(i+1))

            value_list = [best_values[i]]*maxgen
            plt.plot(value_list,"--",label = "best value",linewidth = 0.5)

            value_list = as_foa.as_foa_for_knapsack(maxgen,0.5,problem)
            #plt.plot(as_foa.left_value_list,label = "as_foa(B part)",linewidth = 1)
            plt.plot(value_list,label = "as_foa",linewidth = 1)
            as_foa_values[i].append(max(value_list))
            print("as_foa",max(value_list))

            value_list = as_foa.foa_for_knapsack(maxgen,0.1,problem)
            plt.plot(value_list,label = "foa",linewidth = 1)
            foa_values[i].append(max(value_list))

            value_list = algos.de_for_knapsack(problem,maxgen)
            value_list = get_max_value_prefix(value_list)
            plt.plot(value_list,label = "de",linewidth = 1)
            de_values[i].append(max(value_list))
            print("de",max(value_list))

            value_list = algos.ga_for_knapsack(problem,maxgen)
            value_list = get_max_value_prefix(value_list)
            plt.plot(value_list,label = "ga",linewidth = 1)
            ga_values[i].append(max(value_list))

            value_list = algos.pso_for_knapsack(problem,maxgen)
            plt.plot(value_list,label = "pso",linewidth = 1)
            pso_values[i].append(max(value_list))

            plt.legend(loc ="lower right")
            plt.ylim(ymin=0,ymax=best_values[i]*1.1)
            plt.xlim(xmin=0)
            
            plt.savefig("output/%d/data_set%d.jpg"%(t+1,i+1))
        print('ok',t)

    # plt.xlabel("iterate times")
    # best_value_list = as_foa.as_foa_for_func(1000,0.1,funcs.funcs[0],30,100,50)
    # plt.plot(list(map(lambda x:math.log10(x),best_value_list)),label="lg(f(x))")
    # plt.plot(list(map(lambda x:math.log10(x),as_foa.steps)),label="lg(r)")
    # plt.legend(loc ="upper right")
    # plt.savefig("output/func.jpg")
    # plt.cla()
    # plt.xlabel("iterate times")
    # plt.plot(as_foa.steps,label="r")
    # plt.legend(loc ="upper right")
    # plt.savefig("output/r.jpg")

    for i in range(len(problems)):
        print("data set",i+1)

        print("as_foa")
        print("max",np.max(as_foa_values[i]))
        print("mean",np.mean(as_foa_values[i]))
        print("var",np.var(as_foa_values[i]))

        print("foa")
        print("max",np.max(foa_values[i]))
        print("mean",np.mean(foa_values[i]))
        print("var",np.var(foa_values[i]))

        print("de")
        print("max",np.max(de_values[i]))
        print("mean",np.mean(de_values[i]))
        print("var",np.var(de_values[i]))

        print("ga")
        print("max",np.max(ga_values[i]))
        print("mean",np.mean(ga_values[i]))
        print("var",np.var(ga_values[i]))

        print("pso")
        print("max",np.max(pso_values[i]))
        print("mean",np.mean(pso_values[i]))
        print("var",np.var(pso_values[i]))