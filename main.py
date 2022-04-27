import math
from pickletools import optimize
import backpack_problem
import as_foa
import de
import matplotlib.pyplot as plt
import os

best_values = [295.3,1024,3069,8362,5183,15170,2397,2460]
optimize = True
maxgen = 500 if optimize else 2000

if __name__ == "__main__":
    plt.figure(figsize=(15,20),dpi=300)
    plt.subplots_adjust(hspace=0.3)
    problems = backpack_problem.read_backpack_problems(optimize)
    for i,problem in enumerate(problems):
        pop_size = maxgen
        max_value = 0
        plt.subplot((len(problems)+1)//2,2,i+1)
        plt.xlabel('iterate times')
        plt.ylabel('best value')
        plt.title('data set %d'%(i+1))
        value_list = [best_values[i]]*maxgen
        plt.plot(value_list,"--",label = "best value")
        # value_list = de.de_for_backpack(maxgen,problem)
        # plt.plot(value_list,label = "de")
        # print("de:",value_list[-1])
        value_list = as_foa.as_foa_for_backpack(maxgen,0.1,pop_size,problem)
        plt.plot(value_list,label = "as_foa")
        print("as_foa:",max(value_list))
        plt.legend(loc ="lower right")
        plt.ylim(ymin=0,ymax=best_values[i]*1.1)
        plt.xlim(xmin=0)
        
    os.makedirs("output",exist_ok=True)
    plt.savefig("output/values.jpg")
    

