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
import numpy as np

#OLS

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

    RegressionGPModel  = gp.Model("RegressionReplacement")
    # This sets the model to handle squaring the error equation.
    RegressionGPModel.Params.NonConvex = 2
    # These are the intercept and slope in a regression.  
    b_0 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_1")
    
    # This objective equariont squares the error to immitate an Ordinary Least Squares (OLS) regression.
    start = time.time()
    RegressionGPModel.setObjective(quicksum( (Y[i] - b_1*X[i] - b_0)*(Y[i] - b_1*X[i] - b_0)for i in range(len(X))), GRB.MINIMIZE)

    RegressionGPModel.optimize()
    end = time.time()
    SysMeasureRuntime = end - start
    GurMeasureRuntime = RegressionGPModel.Runtime

   
    
    print("\nGurobi coefficients and error for OLS immitation.")

    # This loop prints the values for each decision variable in the model.
    for v in RegressionGPModel.getVars():
        print( v.Varname, v.x)

    # This prints the final value of the objective function.
    print('SSerror:', RegressionGPModel.ObjVal)
    print("Gurobi measured run time for Gurobi: %f" % GurMeasureRuntime)
    print("System measured run time for Gurobi: ", SysMeasureRuntime)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
    
start = time.time()
Data = pd.DataFrame({'X': X,
                                        'Y':Y
                                        })

BasicRegData = Data.copy()

X = BasicRegData['X'].values.reshape(-1,1)
Y = BasicRegData['Y'].values.reshape(-1,1)
reg = LinearRegression().fit( X, Y)
end = time.time()
print("\nPython OLS regression with sklearn package.")
print("Intercept: ", round(reg.intercept_[0], 5))
print("Coefficient: ", [round(coef, 5) for coef in reg.coef_[0]])
print("Total time", end-start )
