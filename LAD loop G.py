from gurobipy import GRB, quicksum
import gurobipy as gp
import pandas as pd
import math
import time

#Least Absolute Distance (LAD) loop time with Gurobi

try:
    #Get a dataset from XYregData.csv in Github
    #url = 'https://raw.githubusercontent.com/CharnviLopez/RegressionOptimization/main/XYregData.csv?token=GHSAT0AAAAAACK5BZDY6OOBVL2YHUB3H7LOZLU2EPQ'
    #Data = pd.read_csv(url)
    #Student 1 computer
    #Data = pd.read_csv("C:/RegressionOptimizationFoyer/RegressionOptimization/XYregData.csv")
    #Data = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
    #Student 2 computer
    Data = pd.read_csv("/Users/Crow/Desktop/POR/XYregData.csv")
    
    # Assign name for Gurobi
    RegressionGPModel  = gp.Model("RegressionReplacement")
    
    #Silence Gurobi Code
    RegressionGPModel.setParam('OutputFlag', 0)
    
    # These are the intercept(b_0) and coefficient(b_1) in a regression.  
    b_0 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_1")
    
    #Timer start
    start = time.time()
    #Data range input, and start of loop
    for i in range(99):
        X = Data.iloc[0:i,0]
        Y = Data.iloc[0:i,1]
        
        # These variable allow Gurobi to interpret an absolute value for the regression error.
        z = RegressionGPModel.addVars( range(len(X)), vtype = "C", lb = -GRB.INFINITY, name = "z")
        z_1 = RegressionGPModel.addVars( range(len(X)), vtype = "C", name = "z_1")
        z_2 = RegressionGPModel.addVars( range(len(X)), vtype = "C", name = "z_2")
        
        # This allows for a LAD regression method.
        RegressionGPModel.addConstrs(z[i] == (Y[i] - b_1*X[i] - b_0) for i in range(len(X)))
        RegressionGPModel.addConstrs(z[i] == z_1[i] - z_2[i] for i in range(len(X)))
        
        #Gurobi runs the LAD regression
        RegressionGPModel.setObjective(quicksum(z_1[i] + z_2[i] for i in range(len(X))), GRB.MINIMIZE)
        RegressionGPModel.optimize()
        
        #Print i to know which regression it's on
        print(i)
        
    #Timer stop
    end = time.time()
    SysMeasureRuntime = end - start
    
    #Print the run time
    print("System measured run time for Gurobi: ", SysMeasureRuntime)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
