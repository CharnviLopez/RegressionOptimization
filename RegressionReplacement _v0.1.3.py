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
    #Data = pd.read_csv("https://raw.githubusercontent.com/CharnviLopez/RegressionOptimization/main/XYregData.csv?token=GHSAT0AAAAAACIOX3BLMTMZHFCAKKVLQENKZKCZHZA")
    Data = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
    #TwoVarData = Data.iloc[:,0:1]
    X = Data.iloc[0:99,0]
    Y = Data.iloc[0:99,1]

    print ("Len X: ", len(X), sep = "")
    
    print ("Len Y:  ", len(Y), sep = "")
    
    for i in range(len(X)): 
        print("X",i,": ",X[i], sep = "")
    
    for i in range(len(Y)):
        print("Y",i,": ",Y[i], sep = "")
    

    
    # This names the model after its task
    RegressionGPModel  = gp.Model("RegressionReplacement")
    RegressionGPModel.Params.NonConvex = 2
    # These are the intercept and slope in a regression.  
    b_0 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_1")
    
    # These variable allow Gurobi to interpret an absolute value for the regression error.
    z = RegressionGPModel.addVars( range(len(X)), vtype = "C", lb = -GRB.INFINITY, name = "z")
    z_1 = RegressionGPModel.addVars( range(len(X)), vtype = "C", name = "z_1")
    z_2 = RegressionGPModel.addVars( range(len(X)), vtype = "C", name = "z_2")
    
    
    #RegressionGPModel.addConstrs(z[i] == (Y[i] - b_1*X[i] - b_0)*(Y[i] - b_1*X[i] - b_0) for i in range(len(X)))
    #Won't run with a squared term.
    #RegressionGPModel.addConstrs(z[i] == (Y[i] - b_1*X[i] - b_0)^2 for i in range(len(X)))
    RegressionGPModel.addConstrs(z[i] == z_1[i] - z_2[i] for i in range(len(X)))
    
    
    

    RegressionGPModel.setObjective(quicksum(z_1[i] + z_2[i] for i in range(len(X))), GRB.MINIMIZE)

    # This function runs the optimization.
    RegressionGPModel.optimize()
    Data = pd.DataFrame({'X': X,
                                          'Y':Y
                                          })

    BasicRegData = Data.copy()

    X = BasicRegData['X'].values.reshape(-1,1)
    Y = BasicRegData['Y'].values.reshape(-1,1)

    reg = LinearRegression().fit( X, Y)
    print("\nBasic regression with given data.")
    print("Intercept: ", round(reg.intercept_[0], 3))
    print("Coefficient: ", [round(coef, 2) for coef in reg.coef_[0]])

    
    print("\n","\n","This is a solution for regression replacement.")

    # This loop prints the values for each decision variable in the model.
    for v in RegressionGPModel.getVars():
        print( v.Varname, v.x)

    # This prints the final value of the objective function.
    print('Obj:', RegressionGPModel.ObjVal)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
    
