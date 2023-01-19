# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 13:23:11 2023

@author: filon
"""

import numpy as np
import matplotlib.pyplot as plt
import random

def randRocksOnGrid(p,num):
    prob = p
    n = num
    x = np.arange(n)
    y = np.arange(n)
    x1 = []
    y1 = []
    for i in range(len(x)):
        for j in range(len(y)):
            if random.randrange(0,100) <= prob:
                x1.append(x[i])
                y1.append(y[j])
            else:
                continue

    #print(x1)
    #print(y1)
    plt.scatter(x1,y1);
    plt.grid(visible = True, which = 'both');
    plt.xticks(x);
    plt.yticks(y);
    
    return x1, y1