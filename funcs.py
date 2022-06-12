import numpy as np
import math
import random

def func1(x:np.ndarray):
    x = np.square(x)
    return x.sum()

def func2(x:np.ndarray):
    x = np.square(x) - 10*np.cos(2*math.pi*x) + 10
    return x.sum()

def func3(x:np.ndarray):
    return -math.exp(-0.5*func1(x)) + 1

def func4(x:np.ndarray):
    return (np.arange(1,x.shape[0]+1)*(x**4)).sum() + random.random()

def func5(x:np.ndarray):
    return abs(x).sum() + abs(x).prod()

def func6(x:np.ndarray):
    return abs(x*np.sin(x) + 0.1*x).sum()

def func7(x:np.ndarray):
    return func1(x)/4000 - np.cos(x/(np.arange(1,x.shape[0]+1)**0.5)).prod() + 1

def func8(x:np.ndarray):
    return np.power(abs(x),np.arange(2,x.shape[0]+2)).sum()

funcs = [func1,func2,func3,func4,func5,func6,func7,func8]
bounds = [100.0,5.12,1.0,1.28,10.0,10.0,600.0,1.0]