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


try:
    #Get a dataset
    #Data = pd.read_csv('https://raw.githubusercontent.com/CharnviLopez/RegressionOptimization/main/XYregData.csv?token=GHSAT0AAAAAACIS7AIDODH2CNBH63XFCHL4ZKMKLGQ')
    Data = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
    #TwoVarData = Data.iloc[:,0:1]
    X = Data.iloc[0:99,0]
    Y = Data.iloc[0:99,1]

    #print ("Len X: ", len(X), sep = "")
    
    #print ("Len Y:  ", len(Y), sep = "")
    
    #for i in range(len(X)): 
        #print("X",i,": ",X[i], sep = "")
    
    #for i in range(len(Y)):
       # print("Y",i,": ",Y[i], sep = "")
    


    # This names the model after its task.
    RegressionGPModel  = gp.Model("RegressionReplacement")
    # This sets the model to handle squaring the error equation.
    RegressionGPModel.Params.NonConvex = 2
    # These are the intercept and slope in a regression.  
    b_0 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_1")
    
    # These variable allow Gurobi to interpret an absolute value for the regression error.
    #z = RegressionGPModel.addVars( range(len(X)), vtype = "C", lb = -GRB.INFINITY, name = "z")
    #z_1 = RegressionGPModel.addVars( range(len(X)), vtype = "C", name = "z_1")
    #z_2 = RegressionGPModel.addVars( range(len(X)), vtype = "C", name = "z_2")
    
    # This squares the error to immitate a Best Least Squares (BLS)
    #RegressionGPModel.addConstrs(z[i] == (Y[i] - b_1*X[i] - b_0)*(Y[i] - b_1*X[i] - b_0) for i in range(len(X)))
    #Won't run with a squared term.
    #RegressionGPModel.addConstrs(z[i] == (Y[i] - b_1*X[i] - b_0)^2 for i in range(len(X)))
    #RegressionGPModel.addConstrs(z[i] == z_1[i] - z_2[i] for i in range(len(X)))
    
    
    

    #RegressionGPModel.setObjective(quicksum(z_1[i] + z_2[i] for i in range(len(X))), GRB.MINIMIZE)
    #RegressionGPModel.setObjective(quicksum(z[i]for i in range(len(X))), GRB.MINIMIZE)
    RegressionGPModel.setObjective(quicksum( (Y[i] - b_1*X[i] - b_0)*(Y[i] - b_1*X[i] - b_0)for i in range(len(X))), GRB.MINIMIZE)
    # This function runs the optimization.
    RegressionGPModel.optimize()
    
    #This function tell us a more detaild time
    runtime = RegressionGPModel.Runtime
    print("The run time is %f" % runtime)
    
    Data = pd.DataFrame({'X': X,
                                          'Y':Y
                                          })

    BasicRegData = Data.copy()

    X = BasicRegData['X'].values.reshape(-1,1)
    Y = BasicRegData['Y'].values.reshape(-1,1)
   
    print("\n","\n","This is a solution for regression replacement.")

    # This loop prints the values for each decision variable in the model.
    for v in RegressionGPModel.getVars():
        print( v.Varname, v.x)

    # This prints the final value of the objective function.
    print('Obj:', RegressionGPModel.ObjVal)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
    
start = time.time()
reg = LinearRegression().fit( X, Y)
end = time.time()
print("\nBasic regression with given data.")
print("Intercept: ", round(reg.intercept_[0], 3))
print("Coefficient: ", [round(coef, 2) for coef in reg.coef_[0]])
print("Total time", end-start )

# Add constant for intercept term
K = sm.add_constant(X)

# LAD regression using statsmodels with HuberT norm (robust to outliers)
lad_model = sm.RLM(Y, K, M=sm.robust.norms.HuberT()).fit()
print("Coefficients:", lad_model.params[1:]) 
print("Intercept:", lad_model.params[0]) 

predictions = reg.predict(X)  # Predict using the trained model
print("Predictions:")
print(predictions)

predictions = lad_model.predict(K)

# Display the predictions
print("Predictions for original data X:")
print(predictions)
