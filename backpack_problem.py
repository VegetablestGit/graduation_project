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

    #根据重量从小到大排序
    def sort(self): 
        self.items.sort(key= lambda item:item.weight)
