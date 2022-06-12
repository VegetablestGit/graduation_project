from pickletools import optimize
from typing import List
import numpy as np
import random

class KnapsackProBlem:
    def __init__(self,values:np.ndarray,weights:np.ndarray,weight_limit:float) -> None:
        self.weights = weights
        self.values = values
        self.weight_limit:float = weight_limit
        self.optimize = optimize
        self.sort()

    #根据性价比从小到大排序
    def sort(self): 
        items = list(zip(self.values,self.weights))
        items.sort(key = lambda item:item[0]/item[1])
        self.values = np.array([i[0]for i in items])
        self.weights = np.array([i[1]for i in items])
    
    def len(self):
        return len(self.weights)

    def calc(self,pos):
        sorted_pos = list(enumerate(pos))
        sorted_pos.sort(key=lambda p:p[1],reverse=True)
        weight,value = 0,0
        for p in sorted_pos:
            if self.weights[p[0]]+weight > self.weight_limit:
                break
            weight += self.weights[p[0]]
            value += self.values[p[0]]
        return value

    
    #计算重量并优化pos 多退少补
    def calc_value_and_optimise(self,pos)->float:
        pos = np.array(pos)
        value = np.where(pos>=0.5,self.values,np.zeros_like(pos)).sum()
        weight = np.where(pos>=0.5,self.weights,np.zeros_like(pos)).sum()

        if weight > self.weight_limit: #多退
            for i,x in enumerate(pos): 
                if x >= 0.5:
                    #pos[i] = 0.49
                    weight -= self.weights[i]
                    value -= self.values[i]
                if weight <= self.weight_limit:
                    return value
        else: #少补
            for i,x in reversed(list(enumerate(pos))): 
                if x < 0.5 and weight + self.weights[i] <= self.weight_limit:
                    #pos[i] = 0.51
                    weight += self.weights[i]
                    value += self.values[i]
        return value

def read_knapsack_problems()->List[KnapsackProBlem]:
    problems = []
    with open("test.txt") as f:
        while True:
            weight_limit = f.readline()
            if weight_limit == '':
                break
            weight_limit = int(weight_limit)
            values = list(map(float,f.readline().split(',')))
            weights = list(map(float,f.readline().split(',')))
            problems.append(KnapsackProBlem(values,weights,weight_limit))
    return problems
