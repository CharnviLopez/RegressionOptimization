from sklearn.linear_model import LinearRegression
from sklearn.metrics._plot import regression
from gurobipy import GRB, quicksum
import array
import gurobipy as gp
import numpy as np
import scipy.sparse as sp
import pandas as pd
import math
import time
import statsmodels.api as sm


#LAD

try:
    #Get a dataset
    #Data = pd.read_csv('https://raw.githubusercontent.com/CharnviLopez/RegressionOptimization/main/XYregData.csv?token=GHSAT0AAAAAACIS7AIDODH2CNBH63XFCHL4ZKMKLGQ')
    #Data = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
    Data = pd.read_csv("C:/RegressionOptimizationFoyer/RegressionOptimization/XYregData.csv")
    #TwoVarData = Data.iloc[:,0:1]
    X = Data.iloc[0:99999,0]
    Y = Data.iloc[0:99999,1]

    #print ("Len X: ", len(X), sep = "")
    #print ("Len Y:  ", len(Y), sep = "")
    #for i in range(len(X)): 
        #print("X",i,": ",X[i], sep = "")
    #for i in range(len(Y)):
       # print("Y",i,": ",Y[i], sep = "")

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
    print(v[0])
    print(v[1])
    print('SSerror:', RegressionGPModel.ObjVal)
    print("Gurobi measured run time for Gurobi: %f" % GurMeasureRuntime)
    print("System measured run time for Gurobi: ", SysMeasureRuntime)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
    
start = time.time()
# Add constant for intercept term
K = sm.add_constant(X)

# LAD regression using statsmodels with HuberT norm (robust to outliers)
lad_model = sm.RLM(Y, K, M=sm.robust.norms.HuberT()).fit()
end = time.time()
print("\nPython LAD regression with statsmodels package.")
print("Coefficients:", lad_model.params[1:]) 
print("Intercept:", lad_model.params[0]) 
print("Total time", end-start )



#predictions = reg.predict(X)  # Predict using the trained model
#print("Predictions:")
#print(predictions)

#predictions = lad_model.predict(K)

# Display the predictions
#print("Predictions for original data X:")
#print(predictions)
