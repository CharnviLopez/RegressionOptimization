from sklearn.linear_model import LinearRegression
from sklearn.metrics._plot import regression
from gurobipy import GRB, quicksum
import array
import gurobipy as gp
import numpy as np
import scipy.sparse as sp
import pandas as pd
import math


try:
    #Get a dataset
    #Data = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
    #TwoVarData = Data.iloc[:,0:1]
    X = range(10)
    Y = range(10)

    print ("Len X: ", len(X), sep = "")
    
    print ("Len Y:  ", len(Y), sep = "")
    
    for i in range(len(X)): 
        print("X",i,": ",X[i], sep = "")
    
    for i in range(len(Y)):
        print("Y",i,": ",Y[i], sep = "")
    
    Data = pd.DataFrame({'X': X,
                                          'Y':Y
                                          })

    BasicRegData = Data.copy() 

    #X = BasicRegData['X'].values.reshape(-1,1)
    #Y = BasicRegData['Y'].values.reshape(-1,1)

    # reg = LinearRegression().fit( X, Y)
    
    # This names the model after its task
    RegressionGPModel  = gp.Model("RegressionReplacement")

    # These are the intercept and slope in a regression.  
    b_0 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_1")
    
    # These variable allow Gurobi to interpret an absolute value for the regression error.
    z = RegressionGPModel.addVars( range(10), vtype = "C", lb = -GRB.INFINITY, name = "z")
    z_1 = RegressionGPModel.addVars( range(10), vtype = "C", name = "z_1")
    z_2 = RegressionGPModel.addVars( range(10), vtype = "C", name = "z_2")
    
    
    RegressionGPModel.addConstrs(z[i] == Y[i] - b_1*X[i] - b_0 for i in range(10))
    RegressionGPModel.addConstrs(z[i] == z_1[i] - z_2[i] for i in range(10))
    
    RegressionGPModel.setObjective(quicksum(z_1[i] + z_2[i] for i in range(10)), GRB.MINIMIZE)

    # This function runs the optimization.
    RegressionGPModel.optimize()
    
    # print("\nBasic regression with given data.")
    # print("Intercept: ", round(reg.intercept_[0], 3))
    # print("Coefficient: ", [round(coef, 2) for coef in reg.coef_[0]])

    
    print("/n","/n","This is a solution for regression replacement.")

    # This loop prints the values for each decision variable in the model.
    for v in RegressionGPModel.getVars():
        print('%s %g' % (v.Varname, v.x))
        #print(b_0)

    # This prints the final value of the objective function.
    print('Obj: %g' % RegressionGPModel.ObjVal)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
    
