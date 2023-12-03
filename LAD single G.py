from gurobipy import GRB, quicksum
import gurobipy as gp
import pandas as pd
import math
import time

#LAD single Gurobi

try:
    #Get a dataset
    #Data = pd.read_csv('https://raw.githubusercontent.com/CharnviLopez/RegressionOptimization/main/XYregData.csv?token=GHSAT0AAAAAACK5BZDZIN4H7PNL74J6XCAKZLHM53Q')
    Data = pd.read_csv("C:/RegressionOptimizationFoyer/RegressionOptimization/XYregData.csv")
    X = Data.iloc[0:99,0]
    Y = Data.iloc[0:99,1]

    start = time.time()
    # This names the model after its task.
    RegressionGPModel  = gp.Model("RegressionReplacement")
    
    # These are the intercept and slope in a regression.  
    b_0 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_1")
    
    # These variables allow Gurobi to interpret an absolute value for the regression error.
    z = RegressionGPModel.addVars( range(len(X)), vtype = "C", lb = -GRB.INFINITY, name = "z")
    z_1 = RegressionGPModel.addVars( range(len(X)), vtype = "C", name = "z_1")
    z_2 = RegressionGPModel.addVars( range(len(X)), vtype = "C", name = "z_2")
    
    # This allows for a Least Absolute Distance (LAD) regression method.
    RegressionGPModel.addConstrs(z[i] == (Y[i] - b_1*X[i] - b_0) for i in range(len(X)))
    RegressionGPModel.addConstrs(z[i] == z_1[i] - z_2[i] for i in range(len(X)))
    
    RegressionGPModel.setObjective(quicksum(z_1[i] + z_2[i] for i in range(len(X))), GRB.MINIMIZE)
    
 
    RegressionGPModel.optimize()
    end = time.time()
    SysMeasureRuntime = end - start
    GurMeasureRuntime = RegressionGPModel.Runtime

    
    print("\nGurobi coefficients and error for LAD immitation.")

    # This loop prints the values for each decision variable in the model.
    # for v in RegressionGPModel.getVars():
    #     print( v.Varname, v.x)

    v = RegressionGPModel.getVars()
    print(v[0])
    print(v[1])
    print('SSerror:', RegressionGPModel.ObjVal)
    print("Gurobi measured run time for Gurobi: %f" % GurMeasureRuntime)
    print("System measured run time for Gurobi: ", SysMeasureRuntime)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
