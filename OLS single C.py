from gurobipy import GRB, quicksum
import gurobipy as gp
import pandas as pd
import math
import time
import numpy as np
from sklearn.linear_model import LinearRegression

#Ordinary Least Squares (OLS) regression comparison, Python vs Gurobi.

try:
    #Get a dataset from XYregData.csv in Github
    #url = 'https://raw.githubusercontent.com/CharnviLopez/RegressionOptimization/main/XYregData.csv?token=GHSAT0AAAAAACK5BZDY6OOBVL2YHUB3H7LOZLU2EPQ'
    #Data = pd.read_csv(url)
    #Student 1 computer
    Data = pd.read_csv("C:/RegressionOptimizationFoyer/RegressionOptimization/XYregData.csv")
    #Data = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
    #Student 2 computer
    #Data = pd.read_csv("/Users/Crow/Desktop/POR/XYregData.csv")
    
    #Data range input
    X = Data.iloc[0:99,0]
    Y = Data.iloc[0:99,1]

    # Assign name for Gurobi
    RegressionGPModel  = gp.Model("RegressionReplacement")
    
     #Silence Gurobi Code
    RegressionGPModel.setParam('OutputFlag', 0)
    
    # This sets the model to handle squaring the error equation.
    RegressionGPModel.Params.NonConvex = 2
    
    # These are the intercept(b_0) and coefficient(b_1) in a regression.    
    b_0 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_1")
    
    #Gurobi runs the OLS regression
    RegressionGPModel.setObjective(quicksum( (Y[i] - b_1*X[i] - b_0)*(Y[i] - b_1*X[i] - b_0)for i in range(len(X))), GRB.MINIMIZE)
    RegressionGPModel.optimize()

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
    
# OLS regression with sklearn package
Xreg = X.values.reshape(-1, 1)
reg = LinearRegression().fit(Xreg,Y)

#Print Gurobi data
v = RegressionGPModel.getVars()
print("Gurobi Intercept:", b_0.X)
print("Gurobi Coefficient:", b_1.X)

#Print Pythone data
print("Python Intercept:", reg.intercept_)
print("Python Coefficients:", reg.coef_)

#Print diffrence
print("Intercept diffrence", b_0.X - reg.intercept_)
print("Intercept diffrence", b_1.X - reg.coef_)
