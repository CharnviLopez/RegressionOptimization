from gurobipy import GRB, quicksum
import gurobipy as gp
import pandas as pd
import math
import time

#LAD loop Gurobi

try:
    #Get a dataset
    #Data = pd.read_csv('https://raw.githubusercontent.com/CharnviLopez/RegressionOptimization/main/XYregData.csv?token=GHSAT0AAAAAACK5BZDZBR2M6XQJWBZLDUUKZLHNFPA')
    Data = pd.read_csv("C:/RegressionOptimizationFoyer/RegressionOptimization/XYregData.csv")

    # This names the model after its task.
    RegressionGPModel  = gp.Model("RegressionReplacement")
    RegressionGPModel.setParam('OutputFlag', 0)
    
    # These are the intercept and slope in a regression.  
    b_0 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_1")
    
    start = time.time()
    for i in range(99):
        X = Data.iloc[0:i,0]
        Y = Data.iloc[0:i,1]
        
        # These variable allow Gurobi to interpret an absolute value for the regression error.
        z = RegressionGPModel.addVars( range(len(X)), vtype = "C", lb = -GRB.INFINITY, name = "z")
        z_1 = RegressionGPModel.addVars( range(len(X)), vtype = "C", name = "z_1")
        z_2 = RegressionGPModel.addVars( range(len(X)), vtype = "C", name = "z_2")
        
        # This allows for a Least Absolute Distance (LAD) regression method.
        RegressionGPModel.addConstrs(z[i] == (Y[i] - b_1*X[i] - b_0) for i in range(len(X)))
        RegressionGPModel.addConstrs(z[i] == z_1[i] - z_2[i] for i in range(len(X)))
    
        RegressionGPModel.setObjective(quicksum(z_1[i] + z_2[i] for i in range(len(X))), GRB.MINIMIZE)
        RegressionGPModel.optimize()
        print(i)
        # for v in RegressionGPModel.getVars():
        #     print( v.Varname, v.x)
    end = time.time()
    SysMeasureRuntime = end - start
    GurMeasureRuntime = RegressionGPModel.Runtime

    print("\nGurobi coefficients and error for OLS immitation.")

    # This loop prints the values for each decision variable in the model.
    # for v in RegressionGPModel.getVars():
    #     print( v.Varname, v.x)

    # This prints the final value of the objective function.
    print('SSerror:', RegressionGPModel.ObjVal)
    print("Gurobi measured run time for Gurobi: %f" % GurMeasureRuntime)
    print("System measured run time for Gurobi: ", SysMeasureRuntime)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
