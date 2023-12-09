from gurobipy import GRB, quicksum
import gurobipy as gp
import pandas as pd
import math
import time

#OLS loop Gurobi

try:
    #Get a dataset
    #Data = pd.read_csv('https://raw.githubusercontent.com/CharnviLopez/RegressionOptimization/main/XYregData.csv?token=GHSAT0AAAAAACK5BZDYRMKKQHMYE3Q3HWLMZLHMAQA')
    #Data = pd.read_csv("C:/RegressionOptimizationFoyer/RegressionOptimization/XYregData.csv")
    Data = pd.read_csv("/Users/Crow/Desktop/POR/XYregData.csv")
    
    RegressionGPModel  = gp.Model("RegressionReplacement")
    # This sets the model to handle squaring the error equation.
    RegressionGPModel.Params.NonConvex = 2
    # These are the intercept and slope in a regression.  
    b_0 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_1")
    
    # This objective equariont squares the error to immitate an Ordinary Least Squares (OLS) regression.

    start = time.time()
    for i in range(99):
        X = Data.iloc[0:i,0]
        Y = Data.iloc[0:i,1]
        RegressionGPModel.setObjective(quicksum( (Y[i] - b_1*X[i] - b_0)*(Y[i] - b_1*X[i] - b_0)for i in range(len(X))), GRB.MINIMIZE)
        RegressionGPModel.optimize()
        for v in RegressionGPModel.getVars():
            print( v.Varname, v.x)
    end = time.time()
    SysMeasureRuntime = end - start
    GurMeasureRuntime = RegressionGPModel.Runtime

   
    
    print("\nGurobi coefficients and error for OLS immitation.")

    # This prints the final value of the objective function.
    print('SSerror:', RegressionGPModel.ObjVal)
    print("Gurobi measured run time for Gurobi: %f" % GurMeasureRuntime)
    print("System measured run time for Gurobi: ", SysMeasureRuntime)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
