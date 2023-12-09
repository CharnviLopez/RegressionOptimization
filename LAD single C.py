from gurobipy import GRB, quicksum
import gurobipy as gp
import pandas as pd
import math
import time
import statsmodels.api as sm

#LAD single comparison

try:
    #Get a dataset
    #Data = pd.read_csv('https://raw.githubusercontent.com/CharnviLopez/RegressionOptimization/main/XYregData.csv?token=GHSAT0AAAAAACK5BZDZIN4H7PNL74J6XCAKZLHM53Q')
    #Data = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
    Data = pd.read_csv("C:/RegressionOptimizationFoyer/RegressionOptimization/XYregData.csv")
    #Data = pd.read_csv("/Users/Crow/Desktop/POR/XYregData.csv")
    
    X = Data.iloc[0:99,0]
    Y = Data.iloc[0:99,1]

    start = time.time()
    # This names the model after its task.
    RegressionGPModel  = gp.Model("RegressionReplacement")
    
    # These are the intercept and slope in a regression.  
    b_0 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_1")
    
    # These variable allow Gurobi to interpret an absolute value for the regression error.
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
    print("Intercept:", b_0.X)
    print("Coefficients:", b_1.X)
    #print('SSerror:', RegressionGPModel.ObjVal)
    #print("Gurobi measured run time for Gurobi: %f" % GurMeasureRuntime)
    #print("System measured run time for Gurobi: ", SysMeasureRuntime)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
    
start = time.time()
# Add constant for intercept term
K = sm.add_constant(X)

# LAD regression using statsmodels with HuberT norm (robust to outliers)
lad_model = sm.RLM(Y, K, M=sm.robust.norms.HuberT()).fit()
end = time.time()

#print("\nPython LAD regression with statsmodels package.")
#print("Total time", end-start )
#print(lad_model.summary())
intercept = lad_model.params[0]
coefficient = lad_model.params[1:]

print("Intercept:", intercept)
print("Coefficients:", coefficient)

print("Intercept diffrence", b_0.X - intercept)
print("Intercept diffrence", b_1.X - coefficient)