# -*- coding: utf-8 -*-
import numpy as np
import random
from random import randint
import matplotlib.pyplot as plt
import pandas as pd
from numpy import genfromtxt
import os

random.seed(0)
def pla(df_x,df_y):
    iteration = 5
    i = 0
    num_var = df_x.shape[1]
    N = df_x.shape[0]
    rand_w = np.zeros([num_var+1])
    rand_w[0] = 1
    avg_disagreement_p = 0
    best_num_mis_points = N
    best_weight = rand_w
    #add 1s as the first column of x to be the same dim as rand_w
    df_x_augmented = np.ones([N,num_var+1])
    df_x_augmented[:,1:num_var+1] = df_x 
    while i < iteration:
        print "iteration ", i
       #pick a point randomly from all points
       #first iteration just randomly pick one label and its x and add it to rand_w
        if i == 0:
            rand = randint(0,N-1)
            rand_x = df_x_augmented[rand,:]
            rand_w += [j * df_y[rand] for j in rand_x]  
            #print rand_w
        else:
            #calculatate misclassified points
            mis_pts = misclassified_pts( N , rand_w , df_x_augmented )
            #print mis_pts
            num_mis_pts = len( mis_pts )
            if  num_mis_pts == 0:
                print "converged in "+str(i)+" iterations!"
                best_weight = rand_w
                best_num_mis_points = 0
                break
            #if dont converge, update rand_w by randomly pick a point from misclassified points and add to rand_w
            else:
                print "number of misclassified points ", num_mis_pts
                if num_mis_pts < best_num_mis_points:
                    best_num_mis_points = num_mis_pts
                    best_weight = rand_w
                rand = randint(0,len(mis_pts)-1)
                rand_x = df_x_augmented[ mis_pts[rand],: ]
                rand_w += rand_x * df_y[ mis_pts[rand] ]     
                #print rand_w
        i+=1
    return i, best_weight, best_num_mis_points
def misclassified_pts(N, rand_w , df_x_augmented):
    mis_pts = []
    i = 0
    #calculate the score for this iteration/run and compare them with the ground truth df_y
    labels_this_run = np.sign(df_x_augmented.dot(rand_w)) 
    while i < N:
        if labels_this_run[i] != df_y[i]:
            #saving the indexes of misclassified pts
            #print i
            mis_pts.append(i)
        i+=1
    #outputs a set of misclassified points
    return mis_pts 

os.chdir('C:/Users/Beryl/Desktop/UCLA/Courses/Fall2016/BIOSTAT/midtermProject')
df =genfromtxt('./GermanCredit.csv', delimiter=',')
df = df[1:df.shape[0]]
df_y = df[:,24]
df_x = df[:,0:24]
#df_y can't have 0, should turn 0 to -1
for i in range(df_y.shape[0]):
    if df_y[i] == 0:
        df_y[i] = -1
iteration, best_weight, best_num_mis_points = pla(df_x,df_y)
"""
df_train = df[0:900]
df_test = df[900:1000]
df_train_x = np.zeros([,])##set the first column 1 and the rest is df_train[:,0:24]
df_train_x = df_train[:,0:24]
df_train_y = df_train[:,24]
df_test_x = df_test[:,0:24]
df_test_y = df_test[:,24]
"""
