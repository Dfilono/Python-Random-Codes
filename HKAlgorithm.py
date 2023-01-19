# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 13:26:50 2023

@author: filon
"""

import numpy as np
import matplotlib.pyplot as plt

def Matrix(L, p): #Matrix of ones and zeros
    r = np.random.rand(L, L)
    R = np.zeros((L, L))
    for i in range(0, L):
        for j in range(0, L):
            if r[i, j] <= p:
                R[i, j] = 1
            else:
                R[i, j] = 0
    return R

def Find(L, a, b, c, d, Lw): #Find elements in a matrix
    x = L[a, b]
    y = L[c, d]
    
    find_rc = Find_plug(L, x, Lw)
    row = find_rc[0]
    col = find_rc[1]
    
    for i in range(len(col)):
        a2 = row[i]
        b2 = col[i]
        L[a2, b2] = y
    return L

def Find_plug(a, b, Lw):
    size = a.shape
    row = np.array([], dtype=np.int64)
    col = np.array([], dtype=np.int64)
    
    for i in range(0,Lw):
        for j in range(0, Lw):
            if a[i, j] == b:
                row = np.append(row, i)
                col = np.append(col, j)
    return [[row], [col]]

def Label(L,p): #Create matrix for clusters
    R = Matrix(L, p)
    d = 1
    label = np.zeros((L, L))
    for i in range(0, L):
        for j in range(0, L):
            if R[i, j]:
                a1 = Above_left(i, j, R)
                above = a1[0]
                left = a1[1]
                
                if left == 0 and above == 0:
                    label[i ,j] = d
                    d = d + 1
                elif left != 0 and above == 0:
                    label[i, j] = label[i, j-1]
                elif left ==0 and above != 0:
                    label[i, j] = label[i-1, j]
                else:
                    Lab_plug = Find(label, i, j-1, i-1, j, L)
                    label = Lab_plug
                    label[i, j] = label[i-1, j]
    return label

def Above_left(i, j, R):
    if i > 0 and j > 0:
        above = R[i-1, j]
        left = R[i, j-1]
    elif i > 0 and j == 0:
        above = R[i-1, j]
        left = 0
    elif i == 0 and j > 0:
        above = 0
        left = R[i, j-1]
    else:
        above = 0
        left = 0
    return (above, left)

def main(): #Executable
    Lw = 10
    p = 0.5
    L = Label(Lw, p)
    print(L)
    plt.imshow(L)
    plt.colorbar()
    plt.show()