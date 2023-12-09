from gurobipy import GRB, quicksum
import gurobipy as gp
import pandas as pd
import math
import time

#Least Absolute Distance (LAD) single time with Gurobi

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

    #Timer start
    start = time.time()
    
    # Assign name for Gurobi
    RegressionGPModel  = gp.Model("RegressionReplacement")
    
    #Silence Gurobi Code
    RegressionGPModel.setParam('OutputFlag', 0)
    
    # These are the intercept(b_0) and coefficient(b_1) in a regression.    
    b_0 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_1")
    
    # These variables allow Gurobi to interpret an absolute value for the regression error.
    z = RegressionGPModel.addVars( range(len(X)), vtype = "C", lb = -GRB.INFINITY, name = "z")
    z_1 = RegressionGPModel.addVars( range(len(X)), vtype = "C", name = "z_1")
    z_2 = RegressionGPModel.addVars( range(len(X)), vtype = "C", name = "z_2")
    
    # This allows for a LAD regression method.
    RegressionGPModel.addConstrs(z[i] == (Y[i] - b_1*X[i] - b_0) for i in range(len(X)))
    RegressionGPModel.addConstrs(z[i] == z_1[i] - z_2[i] for i in range(len(X)))
    
    # This allows for a LAD regression method.
    RegressionGPModel.setObjective(quicksum(z_1[i] + z_2[i] for i in range(len(X))), GRB.MINIMIZE)
    RegressionGPModel.optimize()
    
    #Run time, 
        #First two lines is to stop the timer
        #The last one is read time by Gurobi
    end = time.time()
    SysMeasureRuntime = end - start
    GurMeasureRuntime = RegressionGPModel.Runtime

    #Print Gurobi data
    v = RegressionGPModel.getVars()
    print("Gurobi Intercept:", b_0.X)
    print("Gurobi Coefficient:", b_1.X)
    
    print("Gurobi measured run time for Gurobi: %f" % GurMeasureRuntime)
    print("System measured run time for Gurobi: ", SysMeasureRuntime)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
