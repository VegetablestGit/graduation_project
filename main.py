import math
import backpack_problem
import as_foa
import matplotlib.pyplot as plt



if __name__ == "__main__":
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(15,20),dpi=300)
    plt.tight_layout()
    problems = backpack_problem.read_backpack_problems()
    for i,problem in enumerate(problems):
        value_list = as_foa.as_foa_for_backpack(200,0.1,problem)
        plt.subplot((len(problems)+1)//2,2,i+1)
        plt.xlabel('iterate times')
        plt.ylabel('best value')
        plt.title('date set %d'%(i+1))
        plt.plot(value_list)
        plt.ylim(ymin=0,ymax=value_list[-1]*1.1)
        plt.xlim(xmin=0)
        print(value_list[-1])
    plt.savefig("output/values.jpg")
    

