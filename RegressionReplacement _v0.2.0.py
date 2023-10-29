import array
import gurobipy as gp
from gurobipy import GRB, quicksum
import numpy as np
import scipy.sparse as sp
import pandas as pd
import math
from sklearn.linear_model import LinearRegression
from sklearn.metrics._plot import regression

try:
    #Get a dataset
    # Data = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
    # TwoVarData = Data.iloc[:,0:1]

    # This names the model after its task- Regression by Gurobi
    RegressionGPModel  = gp.Model("RegressionReplacement")

    # These are the intercept and slope in a regression.  
    b_0 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_1")
    
    z = RegressionGPModel.addVar(obj=1, name = "z")
    z_0 = RegressionGPModel.addVar(obj=1, name = "z_0")
    z_1 = RegressionGPModel.addVar(obj=1, name = "z_1")
    
    
    # These are temporary place holders for data which we manipulate.
    TempXi = range(1,31,3)
    TempYi = range(1,11)

    
    BasicRegData = pd.DataFrame({'X': TempXi,
                                                          'Y':TempYi
                                                          })
    X = BasicRegData['X'].values.reshape(-1,1)
    Y = BasicRegData['Y'].values.reshape(-1,1)

    reg = LinearRegression().fit( X, Y)

    RegressionGPModel.addConstrs(TempYi[i]- b_0 - b_1 *TempXi[i] == z for i in range(len(TempXi)))
    
    RegressionGPModel.setObjective(z, GRB.MINIMIZE)
    
    RegressionGPModel.optimize()
    
    print("\nBasic regression with given data.")
    print("Intercept: ", round(reg.intercept_[0], 3))
    print("Coefficient: ", [round(coef, 2) for coef in reg.coef_[0]])

    print("\nThis is a solution for regression replacement.")

    # This loop prints the values for each decision variable in the model.
    for v in RegressionGPModel.getVars():
        print('%s %g' % (v.Varname, v.x))
        #print(b_0)

    # This prints the final value of the objective function.
    print('Obj: %g' % RegressionGPModel.ObjVal)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
    
