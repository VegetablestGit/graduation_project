from typing import List

class BackpackItem:
    def __init__(self,value:float,weight:float) -> None:
        self.value:float = value
        self.weight:float = weight

class BackpackProblem:
    def __init__(self,values:List[float],weights:List[float],weight_limit:float) -> None:
        self.items:List[BackpackItem] = []
        for v,w in zip(values,weights):
            self.items.append(BackpackItem(v,w))
        self.weight_limit:float = weight_limit

    #根据性价比从小到大排序
    def sort(self): 
        self.items.sort(key= lambda item:item.value/item.weight)

def read_backpack_problems()->List[BackpackProblem]:
    problems:List[BackpackItem] = []
    with open("test.txt") as f:
        while True:
            weight_limit = f.readline()
            if weight_limit == '':
                break
            weight_limit = int(weight_limit)
            values = list(map(float,f.readline().split(',')))
            weights = list(map(float,f.readline().split(',')))
            problems.append(BackpackProblem(values,weights,weight_limit))
    return problems
